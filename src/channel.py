import json
import os
from googleapiclient.discovery import build
import isodate

api_key: str = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

        # Получаем информацию о канале по его ID
        channel_data = youtube.channels().list(part='snippet,statistics', id=self.__channel_id).execute()

        # Заполняем атрибуты канала данными из API
        self.title = channel_data['items'][0]['snippet']['title']
        self.description = channel_data['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subscriber_count = channel_data['items'][0]['statistics']['subscriberCount']
        self.video_count = channel_data['items'][0]['statistics']['videoCount']
        self.view_count = channel_data['items'][0]['statistics']['viewCount']

    def __str__(self):
        """ возвращает информацию по шаблону <название_канала> (<ссылка_на_канал>)"""
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        ''' Метод для сложения количества подписчиков у 2 каналов'''
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        ''' Метод для вычитания количества подписчиков 2 каналов'''
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __lt__(self, other):
        ''' Метод для сравнения количества подписчиков у 2 каналов'''
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        ''' Метод для сравнения количества подписчиков у 2 каналов'''
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __gt__(self, other):
        ''' Метод для сравнения количества подписчиков у 2 каналов'''
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        ''' Метод для сравнения количества подписчиков у 2 каналов'''
        return int(self.subscriber_count) >= int(other.subscriber_count)

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """Метод класса для получения объекта для работы с YouTube API"""
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, file_path: str) -> None:
        """Метод для сохранения значений атрибутов в файл в формате JSON"""
        data = {
            'channel_id': self.__channel_id,
            'channel_title': self.title,
            'channel_description': self.description,
            'channel_link': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }
        with open(file_path, 'w', encoding='UTF-8') as f:
            json.dump(data, f)
