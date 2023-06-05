import os, json
from googleapiclient.discovery import build

class Channel:
    """Класс для ютуб-канала"""
    #API_KEY = os.getenv("YT_API_KEY")
    API_KEY = "AIzaSyAhWpNBvT-JtKHFdF0tM1ksiLSNTeT2SKs"
    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.youtube = build('youtube', 'v3', developerKey=self.API_KEY)
        self.__channel_id = channel_id
        self.url = []
        self.channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        for channel_youtube in self.channel['items'][0]['snippet']['thumbnails']:
            self.url.append(self.channel['items'][0]['snippet']['thumbnails'][channel_youtube]['url'])
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        self.channel = json.dumps(self.channel, indent=2, ensure_ascii=False)
        print(f"{self.channel}")

    @property
    def channel_id(self):
        return self.__channel_id


    @classmethod
    def get_service(cls, channel_youtube = 'UC-OVMPlMA3-YCIeg4z5z23A'):
        """Возвращает объект для работы с YouTube API"""
        return cls(channel_youtube)

    def to_json(self, date):
        """Сохраняет значение атрибутов экземпляра"""
        with open(date, 'a') as file:
            file.write(str(self.channel))
