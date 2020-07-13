#!/usr/bin/env python
# coding: utf-8



from cv_utils import read_with_tesseract
from PIL import Image
import time,io
import json
import requests
from bs4 import BeautifulSoup
from cv_utils import read_with_tesseract

# from pprint import pprint
# from IPython.display import display
# from matplotlib import pyplot as plt
# Plot inline
# %matplotlib inline



class AutoLogin(object):
    def __init__(self, arg_dict):
        
        self.login_url = arg_dict['login_url']
        self.captcha_url = arg_dict['captcha_url']
        
        self.user_list = []
        for user in arg_dict['users']:
            self.user_list.append((user['name'], user['password']))
        
        self.sess = []
        
    def login(self, _username, _password):
        self.sess = requests.Session()
        print('start logging user-%s'%(_username))
        self.sess.trust_env = False
        
        r = self.sess.get(self.login_url)
        soup = BeautifulSoup(r.content, 'lxml')

        warn = soup.find('input', id='warn').get('value')
        lt = soup.find('input', {"name":"lt"}).get('value')
        execution = soup.find('input', {"name":"execution"}).get('value')
        _eventId = soup.find('input', {"name":"_eventId"}).get('value')
        submit = soup.find('input', {"name":"submit"}).get('value')

        login_details = {
            'username': _username,
            'password': _password,
            'captcha': '',
            'warn': warn,
            'lt': lt,
            'execution': execution,
            '_eventId':_eventId,
            'submit': submit
        }
        capt_code = self._read_captcha()
        login_details['captcha'] = capt_code

        r_post = self.sess.post(self.login_url, data=login_details)


        # print(r_post.url)
        # print(r_post.status_code)
        # print(r_post.history)
        # pprint(r_post.text)
        # pprint(r_post.text)
        r_soup = BeautifulSoup(r_post.content, 'lxml')     
        title = r_soup.find('title').text
        # print('title:', title)
        
        if '主页' in title:
            print('user-%s log succeed!!!!' %(_username))
        else:
            print('user-%s log fail!!!'%(_username))
                
        
    def run(self):
        
        for msg in self.user_list:
            self.login(msg[0], msg[1])
            try:
                self.login(msg[0], msg[1])
            except:
                print("An exception occurred we reporting user %s"% (msg[0]))
            
        print('Python script completed at ' + self.get_current_time() +  \
                     '\n-----------------------------------------------\n')
        
    @staticmethod
    def get_current_time():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
    def _get_chatcha_obj(self):
        r_captcha = self.sess.get(self.captcha_url)
        img = io.BytesIO(r_captcha.content)
        image = Image.open(img)
        return image

    def _read_captcha(self):
        image = self._get_chatcha_obj()

        # image.save(captcha_file)

        capt_code, image = read_with_tesseract(image)

        # check code
        retry_num = 0
        # there must be 4 numbers in capt_code, we retry 10 times
        while len(capt_code) != 4 and retry_num<10:
            # display(image)
            retry_num += 1
            print("read captcha with error code %s fail, retry %d..."%(capt_code, retry_num))
            time.sleep(0.5)
            image = self._get_chatcha_obj()
            capt_code, image = read_with_tesseract(image)

        if retry_num==10:
            print("fail to log since captcha is too hard!!! ")

        # display(image)
        # print(capt_code)

        return capt_code



if __name__ == '__main__':
    
    arg_dict = json.load(open('arg.json'))
    logger = AutoLogin(arg_dict)
    logger.run()
