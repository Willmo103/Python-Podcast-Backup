import os
import re

from bs4 import BeautifulSoup as Bs
import requests as r
from classes import Episode, PodcastFeed
import json
import shutil


def get_title(rss_url: str) -> str:
    req = r.get(rss_url)
    soup = Bs(req.content, features='xml')
    title: str = soup.find('title').text
    return title


def get_episodes(rss_url: str) -> dict:
    req = r.get(rss_url)
    soup = Bs(req.content, features='xml')
    items = soup.findAll('item')
    episodes: dict = {}
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
        episodes[f'{j}'] = Episode(episode).to_dict()
        j -= 1
    return episodes


def load_sys_variables():
    with open('sys_variables.json', 'r') as f:
        variables = json.load(f)
    return variables


def write_sys_variables(data: dict):
    with open('sys_variables.json', 'w') as f:
        json.dump(data, f)


def set_dir(download_dir: str):
    sys_variables = load_sys_variables()
    sys_variables['download_dir'] = download_dir
    write_sys_variables(sys_variables)


def update_downloaded_urls(data: str):
    sys_variables = load_sys_variables()
    sys_variables['downloaded_urls'] += [data]
    write_sys_variables(sys_variables)


def get_last_download_dir() -> str:
    var = load_sys_variables()
    return var.get('download_dir')


def get_downloaded_items() -> list:
    var = load_sys_variables()
    return var.get('downloaded_urls')


def is_new(url: str) -> bool:
    downloaded = get_downloaded_items()
    if url in downloaded:
        return True
    return False


def load_podcasts():
    with open("podcasts.json", 'r') as file:
        data = json.load(file)
    return data


def write_to_podcasts(data: dict):
    with open("podcasts.json", "w") as f:
        json.dump(data, f)


def write_to_feeds(data: dict):
    with open("rss_feeds.json", "w") as f:
        json.dump(data, f)


def load_feeds():
    with open("rss_feeds.json", 'r') as file:
        data = json.load(file)
    return data


def add_new_feed(rss_url: str):
    data = load_feeds()
    for i in range(1, len(data), 1):
        if data[f'{i}'] == rss_url:
            print("\nThat podcast already exists in your downloads.")
            return
    if data:
        data[f'{len(data) + 1}'] = rss_url
    else:
        data['1'] = rss_url
    write_to_feeds(data)


def create_feed_data(rss_url: str):
    title = get_title(rss_url)
    podcasts = load_podcasts()
    data = PodcastFeed(rss_url)
    data_to_dict = data.to_dict()
    if title not in podcasts:
        podcasts[title] = data_to_dict
    write_to_podcasts(podcasts)


def check_for_new(rss_url: str):
    title = get_title(rss_url)
    podcasts: dict = load_podcasts()
    episode_list: dict = get_episodes(rss_url)
    downloaded_list: dict = podcasts[title]['episodes']
    if len(episode_list) > len(downloaded_list):
        podcasts[title]['episodes'] = episode_list
        write_to_podcasts(podcasts)
        print(f"Episodes of {title} added to the queue")
    else:
        print(f'{title} is up to date.')


def display_podcast_names():
    podcasts = load_podcasts()
    for podcast in podcasts.values():
        print(podcast['title'], flush=True)


def make_new_folder(podcast_title: str):
    path = get_last_download_dir() + '\\'
    filepath = path + podcast_title
    try:
        os.mkdir(filepath)
        print(f"\nCreating folder: '{filepath}'")
        return filepath
    except OSError:
        pass
    return filepath


def download(episode: dict, podcast_title: str):
    episode_title = episode.get('title')
    episode_title = re.sub(r'\W+', '', episode_title)
    path = make_new_folder(podcast_title) + "\\" + episode_title + ".mp3"
    url = episode.get('url')
    items = get_downloaded_items()
    if url not in items:
        response = r.get(url, stream=True)
        if response.status_code == 200:
            response.raw.decode_content = True
            with open(path, "wb") as mp3_file:
                shutil.copyfileobj(response.raw, mp3_file)
                print(episode["title"], flush=True)
                update_downloaded_urls(url)


def download_all():
    podcasts = load_podcasts()
    for podcast in podcasts.values():
        title = podcast.get('title')
        shows = podcast['episodes']
        for show in shows:
            episode = shows[show]
            try:
                download(episode, title)
            except FileNotFoundError:
                print(f"Unable to download {episode['title']}, continuing...")

