# coding=utf-8 #

# I modified this script after I wrote pydownloader
# All changed code are being commented and added new code

import os
import requests
from bs4 import BeautifulSoup
import pydownloader


class BeautifulPicture:
    """Main class"""
    def __init__(self):
        self.httpheaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)\
                        AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}
        self.front_url = 'http://desktopography.net'
        self.folder_path = '/home/francis/下载/doctemp/desktopo'
        # Change this to set your own path.

    def request(self, url):
        """Web request method."""
        r = requests.get(url, headers=self.httpheaders)
        return r

    '''def saveimg(self, url, name, count):
        """Save image from the given url and name."""
        print('[+] Start requesting image', count, '...')
        img = self.request(url)
        print('[+] Start saving image...')
        f = open(name, 'ab')
        f.write(img.content)
        f.close()
        print('[+] Saved successfully.')'''

    def get_image(self):
        """Main method of crawling from the main page to the download page."""
        print('[+] Start connnecting the website frontpage...')
        web_request = self.request(self.front_url)
        tag_li = BeautifulSoup(web_request.text, 'lxml').find_all('li',\
                 class_='menu-item menu-item-type-post_type menu-item-object-page')
        print('[+] Please choose the year of exhibition you want:')
        print('1:2016 2:2015 3:2014  4:2013  5:2012  6:2011')
        print('7:2010 8:2009 9:2008 10:2007 11:2006 12:2005')
        index = int(input())+2
        year = 2019 - index
        savepath = os.path.join(self.folder_path, str(year))
        if os.path.exists(savepath):
            print('[-] Folder existed.')
        else:
            os.makedirs(savepath)
            print('[+] Folder created.')
        #os.chdir(savepath)
        print('[+] Start connecting the exhibition page...')
        sec_url = tag_li[index].contents[0]['href']
        sec_request = self.request(sec_url)
        tag_div = BeautifulSoup(sec_request.text, 'lxml').find_all('div', class_='overlay-background')
        count = 1
        for div in tag_div:
            thr_url = div['href']
            thr_request = self.request(thr_url)
            tag_a = BeautifulSoup(thr_request.text, 'lxml').find('a', target='_blank', string='1920x1080')
            # Change the param 'string' to set the size you want.
            if not tag_a:
                tag_a = BeautifulSoup(thr_request.text, 'lxml').find('a', target='_blank', string='1920X1080')
            img_url = tag_a['href']
            img_type = img_url[-4:]
            tag_name = BeautifulSoup(thr_request.text, 'lxml').find('h2', class_='single-portfolio-title')
            img_name = tag_name.string+img_type
            count_lst = ['(', str(count), ')']
            img_count = ''.join(count_lst)
            #self.saveimg(img_url, img_name, img_count)
            print('[+] Start requesting image', img_count, '...')
            pdl = pydownloader.Downloader(img_url, savepath, img_name, 2)
            pdl.run()
            count += 1

bs = BeautifulPicture()
bs.get_image()
