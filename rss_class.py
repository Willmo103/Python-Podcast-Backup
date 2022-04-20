from dataclasses import dataclass
from bs4 import BeautifulSoup as Bs
import requests as r
import urllib.parse as p
import shutil as s
import os as os

@dataclass
class Episode:

    def __init__(self, episodes: dict):
        self.number = episodes.get('number')
        self.title = episodes.get('title')
        self.description = episodes.get('description')
        self.date_uploaded = episodes.get('date')
        self.link = episodes.get('link')
        self.url = episodes.get('url')

    def is_audio(self) -> bool:
        try:
            return self.url.post_hint == "audio"
        except AttributeError:
            return False


class Rss:

    def __init__(self, rss_url):
        """
        takes an rss item from a podcast feed and creates a
        class representing the information and a list of urls
        for each episode
        :param rss_url:
        """

        self.url = rss_url
        try:
            self.r = r.get(rss_url)
            self.status_code = self.r.status_code
        except Exception as e:
            print("Error fetching the URL: ", rss_url)
            print(e)
        try:
            self.soup = Bs(self.r.content, features='xml')
        except Exception as e:
            print('Could not parse the xml', self.url)
            print(e)
        self.title: str = self.soup.find('title').text
        self.description: str = self.soup.find('description').text

        items = self.soup.findAll('item')
        self.episodes: list = []
        j: int = len(items)
        for i in items:
            itm_url: str = i.find('enclosure')
            url = itm_url['url']
            episode: dict = {'number': f'{j}',
                             'title': i.title.text,
                             'description': i.description.text,
                             "date": i.pubDate.text,
                             "link": i.link.text,
                             "url": url
                             }
            self.episodes += [Episode(episode)]
            j -= 1

