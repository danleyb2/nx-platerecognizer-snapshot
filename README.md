# NX VMS + Platerecognizer Snapshot

Generate thumbnails from motion events on NX VMS and send to Platerecognizer Plate Reader


## Setup 

### 1. Update configs at the top of main.py

From NX VMS Server
```python
NX_API_BASE = 'https://192.168.0.14:7001/'
NX_CAMERA_ID = '420f37f6-8875-6885-9200-11504e61f485'
NX_LOGIN = "admin"
NX_PASSWORD = "############"
```

From Platerecognizer
```python
API_TOKEN = '4805bee1222########################################'
```

### 3. Install requirements.txt and Run script
```bash
python main.py
```

### 2. Configure Camera Rules

Add 2 rules, both triggered by Motion events, to the Camera whose ID is provided above(NX_CAMERA_ID)

a) Bookmark with the tag `motion1`  
b) Make an HTTP request to this http url `http://IP-of-Script:8001/`


New motion events should now show up as thumbnails on your Platerecognizer dashboard


## Links

NX VMS API Endpoints Documentation
https://localhost:7001/static/index.html#/developers/api/ec2/cameraThumbnail

NX VMS API Authentication
https://support.networkoptix.com/hc/en-us/articles/360020373754-Connecting-a-System-to-Nx-Cloud-using-the-API





