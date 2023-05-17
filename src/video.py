import src.api as api
from googleapiclient.errors import HttpError





class Video:
    def __init__(self, id_video: str):
        """Класс для видео с YouTube"""
        self.__id_video = id_video

        # Получаем информацию о видео по его id
        try:
            video_data = api.youtube.videos().list(part='contentDetails,snippet,statistics', id=self.id_video).execute()
            if not IndexError:
                    self.title = video_data['items'][0]['snippet']['title']
                    self.url = f"https://www.youtube.com/watch?v={self.id_video}"
                    self.viewCount = video_data['items'][0]['statistics']['viewCount']
                    self.likeCount = video_data['items'][0]['statistics']['likeCount']
            else:
                self.title = None
                self.url = None
                self.viewCount = None
                self.likeCount = None
        except HttpError:
            self.title = None
            self.url = None
            self.viewCount = None
            self.likeCount = None


    def __str__(self):
        return f'{self.title}'

    @property
    def id_video(self):
        return self.__id_video




class PLVideo(Video):
    """Класс для видео и плей-листа видео с YouTube"""
    def __init__(self, id_video: str, id_playlist: str):
        super().__init__(id_video)
        self.__id_playlist = id_playlist

    @property
    def id_playlist(self):
        return self.__id_playlist

    def __str__(self):
        return f'{super().__str__()}'
