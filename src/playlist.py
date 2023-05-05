import json
import isodate
import src.api as api
import datetime


class PlayList:
    '''Класс для плейлиста с YouTube'''
    def __init__(self, playlist_id: str):
        self.__id_playlist = playlist_id

        # Получаем информацию о плейлисте по его id
        self.playlist_data = api.youtube.playlists().list(id=playlist_id,part='snippet,contentDetails').execute()
        self.title = self.playlist_data['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.__id_playlist}'

        self.playlist_details = api.youtube.playlistItems().list(playlistId=playlist_id, part='contentDetails').execute()
        self.video_list_id = [video['contentDetails']['videoId'] for video in self.playlist_details['items']]
        self.video_response = api.youtube.videos().list(part='contentDetails,statistics',
                                                   id=','.join(self.video_list_id)).execute()


    @property
    def id_playlist(self):
        return self.__id_playlist

    @property
    def total_duration(self):
        total_duration = datetime.timedelta()
        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration


    def show_best_video(self):
        best_video ={'statistics': {'likeCount':0}}

        for video in self.video_response['items']:
            if int(video['statistics']['likeCount']) > int(best_video['statistics']['likeCount']):
                best_video = video
        return f"https://youtu.be/{best_video['id']}"
