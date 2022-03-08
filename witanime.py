import requests
from bs4 import BeautifulSoup as bs
import argparse
import gdown

links = []

parser = argparse.ArgumentParser(description='A test program.')

parser.add_argument("--url", help="Link of anime from witanime web site",
                    default='https://witanime.com/anime/enen-no-shouboutai-ni-no-shou/')

parser.add_argument("--range", help="range of episodes", default='')
args = parser.parse_args()

url = args.url
range = args.range


def scraper(url):
    response = requests.get(url)
    soup = bs(response.content, 'html.parser')
    episodes = soup.select('a.overlay')
    links = []
    for ep in episodes:
        links.append(ep['href'])
    return links


episodes = scraper(url)


def getEpLinks(episodes,):
    links = []
    for ep in episodes:
        response = requests.get(ep)
        soup = bs(response.content, 'html.parser')
        qualities = soup.select(".tab-content .row.display-flex > div")
        highest_quality = qualities[-1]
        # print(highest_quality)
        servers = highest_quality.select("a")
        # print(servers)
        for server in servers:
            if (server.text == 'google drive'):
                links.append(server["href"])
    return links


def download():
    output = "C:\\Users\\hassa\\Desktop\\mov\\{}\\".format(
        url.split('/')[4].replace('-', ' '))
    if(range):
        start = range.split(",")[0]
        end = range.split(",")[1]
        links = getEpLinks(episodes)[int(start)-1: int(end)]
    else:
        links = getEpLinks(episodes)
    print(f'Downloading {len(links)} episodes...')
    for link in links:
        gdown.download(link, output, quiet=False)


download()
