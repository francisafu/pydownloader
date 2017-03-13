# coding=utf-8

# A simple downloader of python
# Author: Francis Fu
# Date: 03-12-2017
# Used by:
# import pydownloader
# pdl = pydownloader.downloader([url],[filepath],[filename],[multi-threading],[debug state])
# pdl.run()


import requests
import logging
import threading
import os
import sys

"""Debug settings"""
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)
_streamlog = logging.StreamHandler()
_streamlog.setLevel(logging.DEBUG)
_formatter = logging.Formatter('%(levelname)s: %(message)s')
_streamlog.setFormatter(_formatter)
_logger.addHandler(_streamlog)


class Downloader:
    """Main Class"""
    def __init__(self, url, fpath, fname='default', threadcount=1, debugstat=False):
        self.url = url
        self.fpath = fpath
        self.fname = fname
        self.threadcount = threadcount
        self.debugstat = debugstat

        if self.fname == 'default':
            self.fname = self.url.split('/')[-1]

        if os.path.exists(self.fpath):
            os.chdir(self.fpath)
        else:
            _logger.debug('Folder does not exist.')
            sys.exit()

        self.f = open(self.fname, mode='wb')

        if not self.debugstat:
            _streamlog.setLevel(logging.ERROR)

        r = requests.head(self.url)
        self.flength = int(r.headers['Content-Length'])

    def __get_range(self):
        """Split data for multi-threading task"""
        franges = []
        offset = self.flength // self.threadcount
        for i in range(self.threadcount):
            if i == self.threadcount-1:
                franges.append((i * offset, ''))
            else:
                franges.append((i * offset, (i + 1) * offset))
        return franges

    def __download(self, start, end):
        """Download and write file"""
        r = requests.get(self.url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)\
                        AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
                                            'Range': 'Bytes=%s-%s' % (start, end), 'Accept-Encoding': '*'})
        self.f.seek(start)
        self.f.write(r.content)

    def run(self):
        """Multi-thread download main method"""
        thread_list = []
        _logger .debug('Start downloading')
        for ran in self.__get_range():
            start, end =ran
            thread = threading.Thread(target=self.__download(start, end))
            thread.start()
            thread_list .append(thread)
        for i in thread_list:
            i.join()
        _logger.debug('Downloaded')
        self.f.close()
