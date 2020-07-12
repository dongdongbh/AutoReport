#!/usr/bin/env python
# coding: utf-8

from cv_utils import read_with_tesseract
from PIL import Image
from selenium import webdriver
import time,io
import json
# from IPython.display import display
# from matplotlib import pyplot as plt
# Plot inline
# %matplotlib inline

class AutoReport(object):
    def __init__(self, arg_dict):
        self.chrome_options = webdriver.ChromeOptions()
        
        self.chrome_options.add_argument("--start-maximized");
        self.chrome_options.add_argument("disable-gpu")
        # OR options.add_argument("--disable-gpu")
    
        self.login_url = arg_dict['login']
        self.report_url = arg_dict['report']
    
        self.driver = None
        
        self.user_list = []
        
        for user in arg_dict['users']:
            self.user_list.append((user['name'], user['password']))
    
    def login(self, _username, _password):
        self.driver = webdriver.Chrome('chromedriver', options=self.chrome_options)
        self.driver.get(self.login_url)
        capt_code = self._read_captcha()

        username = self.driver.find_element_by_id('username')
        password = self.driver.find_element_by_id('password')
        captcha = self.driver.find_element_by_id('captcha')
        
        username.clear()
        password.clear()
        captcha.clear()

        username.send_keys(_username)
        password.send_keys(_password)
        captcha.send_keys(capt_code)
        
        login_button = self.driver.find_element_by_xpath("//*[contains(@class,'btn-submit')]")
        login_button.click()
        
        # to do
        # ---check log status
        
    def post_data(self, _username):
        self.driver.get(self.report_url)
        checkbox = self.driver.find_element_by_xpath("//input[@name='fieldCNS']")
        checkbox.click()
        submit_button = self.driver.find_element_by_xpath("//*[@class='command_button']")
        submit_button.click()
        
        # screenshot 
        screenshot_name = time.strftime("%Y-%m-%d", time.localtime())
        self.driver.save_screenshot(_username + screenshot_name + '.png')
        
        # to do
        # check report status
        
    def run(self):
        for msg in self.user_list:
            try:
                self.login(msg[0], msg[1])
                self.post_data(msg[0])
                time.sleep(3)
                self.close()
            except:
                print("An exception occurred we reporting user %s"% (msg[0]))
            
        print('Python script completed at ' + self.get_current_time() + \
         	 '\n-----------------------------------------------\n')

    def close(self):
        self.driver.quit()
        
    @staticmethod
    def get_current_time():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    def _get_chatcha_obj(self):
        captcha_element = self.driver.find_element_by_xpath("//*[contains(@src,'captcha.jsp')]")
        captcha_io = captcha_element.screenshot_as_png
        image = Image.open(io.BytesIO(captcha_io))
        return image, captcha_element
    
    def _read_captcha(self):
        image, captcha_element = self._get_chatcha_obj()
        # image.save(captcha_file)
        
        capt_code, image = read_with_tesseract(image)

        # check code
        retry_num = 0
        # there must be 4 numbers in capt_code, we retry 10 times
        while len(capt_code) != 4 and retry_num<10:
            # display(image)
            
            retry_num += 1
            # print("read captcha with error code %s fail, retry %d..."%(capt_code, retry_num))
            captcha_element.click()
            time.sleep(0.5)
            image, captcha_element = self._get_chatcha_obj()
            capt_code, image = read_with_tesseract(image)
            
        if retry_num==10:
            print("fail to log since captcha is too hard!!! ")
        else:
            print("seems good, let's log!")

        # display(image)
        # print(capt_code)

        return capt_code



if __name__ == '__main__':
    
    arg_dict = json.load(open('arg.json'))
    reportor = AutoReport(arg_dict)
    reportor.run()


