# Site: https://pokemon.fandom.com/es/wiki/Lista_de_Pok%C3%A9mon_seg%C3%BAn_la_Pok%C3%A9dex_de_Kanto

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://pokemon.fandom.com/es/wiki/Lista_de_Pok%C3%A9mon_seg%C3%BAn_la_Pok%C3%A9dex_de_Kanto'


def get_id(td):
    return td.text

def get_img_url(td):
  img = td.find('img')
  return img.get('data-image-key')

def get_link(td):
  return 'https://pokemon.fandom.com' + td.a.get('href')

def get_name(td):
  return td.a.text

def get_types(tds):
  skills = []
  for td in tds:
    skills.append(td.a.get('title').replace("Tipo ", ""))
  return ','.join(skills)

def start_read():
    req = requests.get(url, headers ={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    })

    soup = BeautifulSoup(req.text, 'lxml')
    table = soup.find('table', attrs = { 'class': 'tabpokemon' })
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')[1:]

    pokemons = []

    for row in rows:
        cols = row.find_all('td')
        id = get_id(cols[1])
        img_uri = get_img_url(cols[2])
        link = get_link(cols[3])
        name = get_name(cols[3])
        skills = get_types(cols[4:])
        pokemons.append({
            'id': id,
            'img_uri': img_uri,
            'link': link,
            'name': name,
            'skills': skills
        })
    
    df = pd.json_normalize(pokemons)
    df.to_csv("pokemons.csv")


if __name__ == '__main__':
    start_read()
