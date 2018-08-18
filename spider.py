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
import time;
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

# !!!!__IMPORTANT__!!!! #
def end():
    os.remove('data'); # Production should delete
    driver.quit();
    db.close();
    quit();


# Page
class Page:
    def __init__(self):
        self.api = 'https://www.mafengwo.cn';
        self.page = 1;
        self.end = None;

    def get_link(self):
        driver.get(self.api);
        
        elems = driver.find_elements_by_xpath("//dt//a")
        for e in elems:
            href = e.get_attribute('href');
            try:
                islink = re.compile('https://www.mafengwo.cn/i/\S*').search(str(href));
                Links.create(page = self.page, link = islink[0]);
            except:
                self.end = True;
                continue;

    def next_page(self):
        try:
            button = driver.find_element_by_xpath("//a[@class='pg-next _j_pageitem']");
            actions.move_to_element(button);
            actions.click(button);
            actions.perform();
            while(True):
                time.sleep(2);

                label = driver.find_element_by_xpath("//a[@class='pg-next _j_pageitem']");
                data = label.get_attribute('data-page');
                if (int(data) == self.page + 2) :
                    self.page += 1;
                    break;

        except:
            print('panic...')
            end();
        


def start():
    pointer = Page();
    while(True):
        p.get_link();
        p.next_page();

        if (p.end == True):
            break;
            
            
# TEST
def test():
    p = Page();
    p.get_link();
    p.next_page();


## l = Links.select().where(Links.page == 1)
## for foo in l:
##     print(foo.link)
test();
end();

