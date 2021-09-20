"""
users will need to run a standalone application that the VMS will send the short video to then the application will retrieve a video and forward to Stream SDK or the API cloud.

Configure 2 rules for the camera on the VMS
a) Bookmark Motion events with a tag
b) Make an HTTP request to notify about motion events
Start Server that listens for the HTTP requests from the camera
When a motion event is received by the server...

"""

import cgi
import json
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
from json.decoder import JSONDecodeError

# Constants
NIX_API_BASE = 'https://localhost:7001/'
NIX_CAMERA_ID = '420f37f6-8875-6885-9200-11504e61f485'

SYSTEM_LOGIN = "admin"
SYSTEM_PASSWORD = "NxWitness"

# End Constants


def main():
    # Retrieve the latest bookmark from the camera to get the motion start timestamp
    # this done through the API
    # TODO order by date desc and limit to 1
    endpoint  = f'{NIX_API_BASE}ec2/bookmarks'
    params = {
        'cameraId' : NIX_CAMERA_ID,
        'filter': 'motion1'
    }


    res = requests.get(
        endpoint,
        params=params,
        auth=requests.auth.HTTPDigestAuth(SYSTEM_LOGIN, SYSTEM_PASSWORD)
    )

    events = res.json()
    if len(events):
        event = events[0]
        start_timestamp = event['startTimeMs']

        # Download an image through API by at the start timestamp
        endpoint2 = f'https://localhost:7001/ec2/cameraThumbnail'
        params2 = {
            'cameraId': NIX_CAMERA_ID,
            'time':start_timestamp,
            'imageFormat':'png',
            'method':'after'
        }

        thumbnail_res = requests.get(
            endpoint2,
            params=params2,
            auth=requests.auth.HTTPDigestAuth(SYSTEM_LOGIN, SYSTEM_PASSWORD)
        )


        # Send the downloaded image to Snapshot API




class GetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        main()

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Event Processed.')
        return


if __name__ == '__main__':
    server = HTTPServer(('', 8001), GetHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
