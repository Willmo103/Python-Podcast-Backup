from bs4 import BeautifulSoup as Bs
import requests as r


class PodcastFeed:

    def __init__(self, rss_url):

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

    def to_dict(self):
        episodes_dict = {}
        for episode in self.episodes:
            episode_data = episode.to_dict()
            episodes_dict[f"{episode.number}"] = episode_data
        podcast_dict = {
            'title': self.title,
            'description': self.description,
            'episodes': episodes_dict
        }
        return podcast_dict


class Episode:

    def __init__(self, episodes: dict):
        self.number = episodes.get('number')
        self.title = episodes.get('title')
        self.description = episodes.get('description')
        self.date_uploaded = episodes.get('date')
        self.link = episodes.get('link')
        self.url = episodes.get('url')

    def to_dict(self):
        episode_dict = {
            'title': self.title,
            'description': self.description,
            'date_Uploaded': self.date_uploaded,
            'link': self.link,
            'url': self.url
        }
        return episode_dict
