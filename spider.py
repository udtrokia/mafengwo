##
 #
 #   mafengwo spider
 #
 #   udtrokia@gmail.com
 #
 ##


# modules
import os;
import re;
import json;
import requests as r;

from peewee import *;
from selenium import webdriver;
from selenium.webdriver.chrome.options import Options;
from selenium.webdriver.common.action_chains import ActionChains;

# DB
db = SqliteDatabase('data');
db.connect();

class Links(Model):
    page = IntegerField();
    link = CharField();

    class Meta:
        database = db;

class Contents(Model):
    date = CharField();
    days = IntegerField();
    toc = CharField();

    class Meta:
        database = db;

db.create_tables([Contents, Links]);


# Driver Set
chrome_options = Options();
chrome_options.add_argument('--headless');
chrome_options.add_argument('--disable-gpu');

driver = webdriver.Chrome(chrome_options=chrome_options);
actions = ActionChains(driver);

# Page
class Page:
    def __init__(self):
        self.api = 'https://www.mafengwo.cn';
        self.page = 1;

    def get_link(self):
        driver.get(self.api);
        
        elems = driver.find_elements_by_xpath("//dt//a")
        for e in elems:
            href = e.get_attribute('href');
            try:
                islink = re.compile('https://www.mafengwo.cn/i/\S*').search(str(href));
                Links.create(page = self.page, link = islink[0]);
            except: continue;
                        
    def next_page(self):
        
        print(dir(driver))



# TEST
p = Page();
p.next_page();

## l = Links.select().where(Links.page == 1)
## for foo in l:
##     print(foo.link)


# !!!!__IMPORTANT__!!!! #
driver.quit();
db.close();
