import logging
import sys
import io
import os
import requests
from requests.auth import HTTPDigestAuth
from http.server import BaseHTTPRequestHandler, HTTPServer


LOG_LEVEL = os.environ.get('LOGGING', 'INFO').upper()

logging.basicConfig(
    stream=sys.stdout,
    level=LOG_LEVEL,
    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
)


# Constants
NX_BOOKMARK_TAG = 'motion1'
NX_API_BASE = 'https://192.168.0.14:7001/'
NX_CAMERA_ID = '420f37f6-8875-6885-9200-11504e61f485'

NX_LOGIN = "username"
NX_PASSWORD = "password@"

API_TOKEN = '4805bee1222###############################'

# End Constants

auth = HTTPDigestAuth(NX_LOGIN, NX_PASSWORD)


def download_bookmarks():
    logging.info(f'Downloading bookmarks')

    bookmarks_endpoint = f'{NX_API_BASE}ec2/bookmarks'
    bookmarks_res = requests.get(
        bookmarks_endpoint,
        params={
            'cameraId' : NX_CAMERA_ID,
            'filter': NX_BOOKMARK_TAG,
            'sortBy':'startTime',
            'sortOrder':'desc',
            'limit':1
        },
        auth=auth,
        verify=False
    )

    logging.info(f'bookmarks_res: {bookmarks_res}')
    return bookmarks_res.json()


def download_thumbnail(start_timestamp):
    logging.info(f'Downloading thumbnail after: {start_timestamp}')

    thumbnail_endpoint = f'{NX_API_BASE}ec2/cameraThumbnail'

    thumbnail_res = requests.get(
        thumbnail_endpoint,
        params={
            'cameraId': NX_CAMERA_ID,
            'time': start_timestamp,
            'imageFormat': 'png',
            'method': 'after'
        },
        auth=auth,
        verify=False,
        stream=True
    )

    logging.info(f'thumbnail_res: {thumbnail_res}')

    return thumbnail_res



def main():
    # Retrieve the latest bookmark from the camera to get the motion start timestamp
    bookmarks = download_bookmarks()

    if len(bookmarks):
        logging.debug('Bookmarks found.')
        bookmark = bookmarks[0]
        start_timestamp = bookmark['startTimeMs']

        thumbnail_res = download_thumbnail(start_timestamp)

        # Send the downloaded image to Snapshot API
        buffer = io.BytesIO(thumbnail_res.content)
        buffer.seek(0)
        plate_reader_response = requests.post(
            # 'http://localhost:8080/v1/plate-reader/',
            'http://api.platerecognizer.com/v1/plate-reader',
            files=dict(upload=buffer),
            headers={
                'Authorization': 'Token ' + API_TOKEN,
            }
            # data=dict(regions=[],
            # camera_id='dz1',
            # config=json.dumps(dict(mode='fast'))
            # )
        )

        logging.info(plate_reader_response.text)
    else:

        logging.info('Bookmarks not found')



class GetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        logging.info('HTTP Event Received.')
        main()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Event Processed.')
        return


if __name__ == '__main__':
    server = HTTPServer(('', 8001), GetHandler)
    logging.info('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
