from googleapiclient.discovery import build
import os


class Video:
    """Функция для получения информации о видео с YouTube"""
    # API_KEY = os.getenv('YT_KEY')
    API_KEY = "AIzaSyAhWpNBvT-JtKHFdF0tM1ksiLSNTeT2SKs"
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, id_video):

        try:
            self.id_video = id_video
            self.video = self.youtube.videos().list(id=self.id_video, part='snippet,statistics').execute()
            self.title = self.video['items'][0]['snippet']['title']
            self.url_video = self.video['items'][0]['snippet']['thumbnails']['default']['url']
            self.count_views = self.video['items'][0]['statistics']['viewCount']
            self.like_count = self.video['items'][0]['statistics']['likeCount']
        except IndexError:
            self.video = None
            self.title = None
            self.url_video = None
            self.count_views = None
            self.like_count = None

    def __str__(self):
        """Функция вывода названия видео"""
        return f"{self.title_video}"


class PLVideo(Video):
    """Наследование от класса Video"""

    def __init__(self, id_video, playlist_id):
        super().__init__(id_video)
        self.playlist_id = playlist_id

    def __str__(self):
        """Функция вывода название видео"""
        return f"{self.title_video}"
