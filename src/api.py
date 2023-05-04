import json
import os
from googleapiclient.discovery import build


api_key: str = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)
