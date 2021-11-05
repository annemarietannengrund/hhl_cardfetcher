from urllib import request
import requests
import os
from bs4 import BeautifulSoup

def parsePage(p=None, link=None, path=None):
    l = link+'/page/'+str(p)
    print(l)
    html = requests.get(l)
    response = BeautifulSoup(html.text, 'html.parser')
    links = response.select('a.thickbox')
    for y, link1 in enumerate(links):
        print(p, link1['href'].split('/')[-1])
        request.urlretrieve(link1['href'], path+'/' + link1['href'].split('/')[-1])

def createDirectory(path):
    try:
        os.makedirs(path)
    except OSError as error:
        print(error)

if __name__ == "__main__":
    html = requests.get('https://www.horusheresylegions.com/legions-card-list/')
    response = BeautifulSoup(html.text, 'html.parser')
    links = response.select('div.wp-block-column > figure.wp-block-image > a')
    linksT = response.select('div.wp-block-column > figure.wp-block-image > figcaption > a')
    titles = []
    for i, link in enumerate(linksT):
        if link.text.strip() != '':
            titles.append(link.text.strip())
    cpath = os.getcwd()
    for i, link in enumerate(links):
        print(i, titles[i],link['href'])
        p = 'img/' + titles[i]
        p = p.replace(':','')
        print('creating {}'.format(p))
        createDirectory(p)

        html = requests.get(link['href'])
        response = BeautifulSoup(html.text, 'html.parser')
        links2 = response.select('div.ngg-album-link > a')
        for k, link2 in enumerate(links2):
            print(k, link2['title'], link2['href'])
            p2 = p + '/' + link2['title']
            p2 = p2.replace(':', '')
            print('creating {}'.format(p2))
            createDirectory(p2)

            for i in range(1,3):
                parsePage(i, link2['href'], p2)
        print('-------------------------------------')
        print('')
