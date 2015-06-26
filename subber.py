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

    def get_sub_fn(self, file):
        folder, fn = os.path.split(file)
        fn = fn[:-3] + 'srt'
        return os.path.join(folder, fn)

    def get_sub(self, vid_file_path):

        params = {
            'hash': self.hash(vid_file_path),
        }

        subs = requests.get(self.url.format(**params), headers=self.headers)
        if subs.status_code == 200:

            with open(self.get_sub_fn(vid_file_path), 'wb') as fout:
                fout.write(subs.content)
        return subs.status_code == 200

#test_file = '/home/yurib/video/12.Monkeys.S01E03.HDTV.x264-KILLERS.mp4'

if __name__ == '__main__':
    subber = SubDB()
    for root, folders, files in os.walk(root_dir):
        for fn in files:
            if fn[-3:] in ['mp4', 'avi', 'mkv']:
                if 'sample' in root.lower():
                    result = 'SKIPPING'
                else:
                    subfn = subber.get_sub_fn(os.path.join(root,fn))
                    subfn_missing = subfn + '.missing'
                    if os.path.isfile(subfn) or os.path.isfile(subfn_missing):
                        result = 'EXISTS'
                    else:
                        got_subs = subber.get_sub(os.path.join(root, fn))
                        if not got_subs:
                            with open(subfn_missing,'w') as fout:
                                fout.write('')
                        result = 'DOWNLOADD' if got_subs else 'NOT_FOUND'
                print '{:<96}{}'.format(fn, result)
