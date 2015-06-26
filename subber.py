__author__ = 'yurib'

import requests
import os
import hashlib

root_dir = '/home/yurib/video'


class SubDB(object):

    useragent = 'SubDB/1.0 (subber/0.1; https://github.com/yuribak/subber)'
    headers = {
        'User-Agent': useragent,
    }
    url = 'http://api.thesubdb.com/?action=download&hash={hash}&language=en'

    hash_read_size = 64 * 1024

    def hash(self, fn):
        with open(fn,'rb') as fin:
            data = fin.read(self.hash_read_size)
            fin.seek(-self.hash_read_size,os.SEEK_END)
            data += fin.read(self.hash_read_size)
        return hashlib.md5(data).hexdigest()

    def get_sub(self, vid_file_path):

        params = {
            'hash': self.hash(vid_file_path),
        }

        subs = requests.get(self.url.format(**params), headers=self.headers)
        if subs.status_code == 200:
            folder, fn = os.path.split(vid_file_path)
            fn = fn[:-3] + 'srt'
            with open(os.path.join(folder, fn), 'wb') as fout:
                fout.write(subs.content)
        return subs.status_code == 200


subber = SubDB()
test_file = '/home/yurib/video/12.Monkeys.S01E03.HDTV.x264-KILLERS.mp4'
print subber.hash(test_file)
print subber.get_sub(test_file)
#for root,folders,files in os.walk(root_dir):
