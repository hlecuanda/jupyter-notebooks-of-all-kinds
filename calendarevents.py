#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CalendarEvents.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1L6dxPKwmy9SsufGnWfrxY05wY4vITnHB

##Auth
"""

import os
import re
import datetime
from time import sleep
from pprint import pprint

#  from google.colab import auth
from googleapiclient.discovery import build
from apiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account

try:
    import uuid0
    from google.cloud import storage
    from googleapiclient import discovery
except:
    #  !pip install --upgrade google-cloud-storage
    #  !pip install --upgrade google-api-client
    #  !pip install --upgrade uuid0
    import uuid0
    from google.cloud import storage
    from googleapiclient import discovery


STORAGE_BUCKET = "archive.h-lo.me"
STORAGE_PATH = "credentials/"
PROJECT = "colab-datalab-nbooks"
SA_FILE = "colab-datalab-nbooks-0b23b6ee2449.json"


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client(PROJECT)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print('Auth credentials  downloaded to {}.'.format(
        destination_file_name))


def reset_credentials():
    os.remove(SA_FILE)


SCOPES = ['https://www.googleapis.com/auth/calendar']

try:
    os.stat(SA_FILE)
except FileNotFoundError:
    download_blob(STORAGE_BUCKET, STORAGE_PATH+SA_FILE, SA_FILE)

credentials = service_account.Credentials.from_service_account_file(
        SA_FILE, scopes=SCOPES).with_subject('hector@lecuanda.com')

# drive  = discovery.build('drive', 'v3', credentials=credentials)
# sheets= discovery.build('sheets','v4', credentials=credentials)
calendar = discovery.build('calendar','v3', credentials=credentials)

"""## Calendar

###  Get phonecalls Calendar
"""

now = datetime.datetime.utcnow()
start = datetime.datetime(now.year,
                          5,
                          1).isoformat() + 'Z' # 'Z' indicates UTC time

PHONECALLS_CALENDAR = 'lecuanda.com_oigsd97meblvho2lcq4fhdvelg@group.calendar.google.com'
TIMINGS_CALENDAR = 'lecuanda.com_pe3pajpic2srsj27aqd4l0qfhs@group.calendar.google.com'



def moveEventsList(eventlist):
    for call in eventlist:
        calendar.events().move(calendarId=PHONECALLS_CALENDAR,
                            eventId = call['id'],
                            destination = TIMINGS_CALENDAR,
                            sendNotifications = False).execute()
        print('moved {}'.format(call['summary']))
        sleep(12)



phonecalls = calendar.events().list(calendarId=PHONECALLS_CALENDAR,
                                       timeMin=start,
                                       #maxResults=20,
                      #                 q='Missed',
                                       singleEvents=True,
                                       orderBy='startTime').execute().get('items',[])

jrmcalls=[]
unknown=[]
m=re.compile('^Meza.*')
u=re.compile('.*Unknown.*')

for call in phonecalls:
    if m.match(call['summary']):
        jrmcalls.append(call)
    if u.match(call['summary']):
        unknown.append(call)

#  print(len(phonecalls))
#  print(len(unknown))
print(len(jrmcalls))
#  pprint(phonecalls)
#  pprint(unknown)
#  pprint(jrmcalls)

moveEventsList(jrmcalls)