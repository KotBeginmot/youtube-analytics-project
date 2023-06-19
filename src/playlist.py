import os
from datetime import timedelta

import isodate
from googleapiclient.discovery import build


class PlayList:
    """Получаем имя плейлиста и ссылку на него"""
    #API_KEY = os.getenv('YT_KEY')
    API_KEY = "AIzaSyAhWpNBvT-JtKHFdF0tM1ksiLSNTeT2SKs"
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.playlist_items = self.youtube.playlists().list(id=self.playlist_id, part='snippet').execute()
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                                 part='contentDetails',
                                                                 maxResults=50,
                                                                 ).execute()
        self.title = self.playlist_items['items'][0]['snippet']['title']
        self.url = "https://www.youtube.com/playlist?list=" + self.playlist_id
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in
                                     self.playlist_videos['items']]
        self.video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                         id=','.join(self.video_ids)
                                                         ).execute()

    def show_best_video(self):
        """Функция возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
        like = []
        id_video = ''
        for i in self.video_response['items']:
            like.append(i['statistics']['likeCount'])
        max_liked = max(like)
        for item in self.video_response['items']:
            if int(item['statistics']['likeCount']) == int(max_liked):
                id_video = item['id']
        return f"https://youtu.be/{id_video}"

    @property
    def total_duration(self):
        """Функция возвращает видео с суммарной длительностью плейлиста, т.е самые длинные"""
        duration = 0
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration += isodate.parse_duration(iso_8601_duration).seconds
        return timedelta(seconds=duration)