import urllib.request, json
from configparser import ConfigParser


def get_config(fn):
    parser = ConfigParser()
    parser.read(fn)
    db = parser.items('db')
    return {name: value for name, value in db}


conf = get_config('config.ini')
api_key = conf['api_key']

q = str(input('Enter something you want 50 gifs of from GIPHY \n').split()[0])

domain = 'api.giphy.com'
search_for = 'gifs'
limit = '50'
offset = '0'
rating = ''
lang = 'en'
url = f'http://{domain}/v1/gifs/search?api_key={api_key}&q={q}&limit={limit}&offset={offset}&rating={rating}&lang={lang}'

urls = []
res = urllib.request.urlopen(url).read().decode('utf-8')
posts = json.loads(res)

data = posts['data']
if len(data) > 1:
    for d in data:
        urls.append(d['url'])
    print(urls)
else:
    print("Sorry, the item that you searched for was not found on GIPHY.com")
