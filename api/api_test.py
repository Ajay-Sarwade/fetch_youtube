from .models import Videos
from fetch_api import settings
from datetime import datetime, timedelta

from googleapiclient.discovery import build
from apiclient.errors import HttpError


def getnewposts():
    apikeys = settings.API_KEYS
    current_time = datetime.now()
    
    req_time = current_time - timedelta(minutes=5)
    

    flag=False
    for apikey in apikeys:
        try:
            

            youtube = build("youtube", "v3", developerKey=apikey)
           
            req = youtube.search().list(q="cricket",part="snippet", order="date",
                                        maxResults=50, publishedAfter=(req_time.replace(microsecond=0).isoformat()+'Z') )
            response = req.execute()
          
            flag=True
            for obj in response['items']:
                title = obj['snippet']['title']
                description = obj['snippet']['description']
                publishingDateTime = obj['snippet']['publishedAt']
                thumbnailsUrls = obj['snippet']['thumbnails']['default']['url']
                channelTitle = obj['snippet']['channelTitle']

                Videos.objects.create(title=title, description=description,
                        publishingDateTime=publishingDateTime, thumbnailsUrls=thumbnailsUrls,
                        channelTitle=channelTitle)

        
        except HttpError as er:
            err_code = er.resp.status
            if not(err_code == 400 or err_code == 403):
                break

        if flag:
            break