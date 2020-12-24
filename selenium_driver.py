# importing the necessary libraries

import selenium 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
import time 
from selenium.webdriver.chrome.options import Options
import random 
from selenium.webdriver.support import expected_conditions as EC
import sys


def wait_until(driver, xpath, waiting_time = 10):
    wait = WebDriverWait(driver, waiting_time)
    
    
def create_driver(url):
    
        
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--profile-directory=Default")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-plugins-discovery")
    
    chrome_options.add_argument('--incognito')
     
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    # driver = webdriver.Chrome(executable_path = 'chromedriver.exe', options= chrome_options ) 
    driver.get(url)
    print('driver intitiated  \n')
    return driver 

# function that will close the cookies warning 
def close_cookies_warning(driver, xpath):
    driver.find_element_by_xpath(xpath).click()
    
    
def get_rss_feed(driver, xpath = '//*[@id="content"]/div/div[2]/div/div[1]/div[2]/p'):
    driver.get('https://startuptimes.net/rss-feeds')
    rss_url = driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[1]/div[2]/p')
    return rss_url.text


def get_all_post_links(driver):
    categories_url = ['https://startuptimes.net/startup-stories', 
                      'https://startuptimes.net/inspirational-stories', 
                      'https://startuptimes.net/news', 
                      'https://startuptimes.net/articles', 
                      'https://startuptimes.net/articles/marketing', 
                      'https://startuptimes.net/articles/schemes', 
                      'https://startuptimes.net/articles/editorial', 
                      'https://startuptimes.net/articles/tech']
    
    result = {
        'links' : [], 
        'titles' : []
        }
    
    all_page_links = []   # will contains the pages of all the links 
    print('extracting all the possible pages of all the categories \n')
    for url in categories_url:
         driver.get(url)
         time.sleep(3)
         
         page_elements = driver.find_elements_by_class_name('page-num')
         for page in page_elements:
             page_link = page.find_element_by_tag_name('a')
             all_page_links.append(page_link.get_attribute('href'))
             
    for url in all_page_links:
        driver.get(url)
        time.sleep(3)
        print('extracting  : ', url)
        title_element = driver.find_elements_by_tag_name('h3')
        for item in title_element:
            link = item.find_element_by_tag_name('a')
            result['links'].append(link.get_attribute('href'))
            result['titles'].append(link.text)
            
    final_result = {
        'links' : [], 
        'titles' : []
        }
    
    for link, title in zip(result['links'], result['titles']):
        if title == '':
            text = link.split('/')[-1].split('-')
            string = ''
            for item in text:                                                  # this code corrects the titles in case it is not available 
                string = string + item + ' '
            final_result['titles'].append(string.strip())
            final_result['links'].append(link)
        else:
            final_result['titles'].append(title.strip())
            final_result['links'].append(link)
   
    # print(len(final_result['links']))     # getting more than expacted values
    # print(len(final_result['titles']))    # getting more than expacted values
    
    unique_titles = []
    unique_links = []
    
    for title, link in zip(final_result['titles'], final_result['links']):
        if title.strip().lower() not in unique_titles:
            unique_titles.append(title.strip().lower())
            unique_links.append(link)
            
        
    return {
        'links' : unique_links, 
        'titles' : unique_titles
        }
                     
def login_to_stackoverflow(driver,
                           user = 'startuptimes.officials@gmail.com', 
                           password = 'abdul@123'):
    
        wait = WebDriverWait(driver, 10)
        print('initiating the stackoverflow ...\n')
        driver.get('https://www.stackoverflow.com/')

        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/header/div/ol[2]/li[2]/a[1]'))).click()
             
        except:
            driver.refresh()
            time.sleep(5)
            driver.close()
            sys.exit() 
        
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="openid-buttons"]/button[1]'))).click()
             
        except:
            # driver.refresh()
            time.sleep(5)
            driver.close()
            sys.exit() 
    
        try:
            email_input_box = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="identifierId"]')))
             
        except:
            driver.close()
            sys.exit() 
           
        time.sleep(2)
        try:
            for item in user:
                email_input_box.send_keys(item)
                time.sleep(random.randint(1, 2))
                # time.sleep(1)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="identifierNext"]/div/button/div[2]'))).click()
                # driver.find_element_by_xpath('//*[@id="identifierNext"]/div/button/div[2]').click()
        except Exception as e:
            
            driver.close()
            sys.exit()
        
        try:
            pass_box = wait.until(EC.presence_of_element_located((By.XPATH, 
                   '//*[starts-with(@id, "password")]/div[1]/div/div[1]/input' )))
            # //*[@id="password"]/div[1]/div/div[1]/input
            # //*[@id="password"]/div[1]/div/div[1]/input
            # //*[@id="password"]/div[1]/div/div[1]/input
            for item in password:
                pass_box.send_keys(item)   
                time.sleep(random.randint(0, 1))
                # starts-with(@id, "passwordNext")
        except:
            try:
                pass_box = wait.until(EC.presence_of_element_located((By.XPATH,
                                                '//*[@id="password"]/div[1]/div/div[1]/input' )))
                # //*[@id="password"]/div[1]/div/div[1]/input
                for item in password:
                    pass_box.send_keys(item)
                    time.sleep(random.randint(0, 2))
            except Exception as e:
                print(e)
                driver.close()
                sys.exit()
                
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[starts-with(@id, "passwordNext")]'))).click()    
        time.sleep(1)
        print('logged in to google successfully ... ')
    

def login_to_blogger_post(driver, feed_link, url = 'https://blogger.com/', 
                     user = 'abdultaufiq1001@gmail.com', 
                     password = 'abdul3567@'):
    wait = WebDriverWait(driver, 10)
    
    driver.get('https://www.blogger.com/blog/layout/6999700223315358396')
    time.sleep(4)

    driver.switch_to.frame('editorframe')
    # time.sleep(3)
    wait.until(EC.element_to_be_clickable((By.ID, 'layout-addgadget'))).click()
    # driver.find_element_by_id('layout-addgadget').click()     # click on add gadget 
    time.sleep(5)
    
    windows = driver.window_handles
    for i, item in enumerate(windows):
        if i == 1:
            driver.switch_to.window(item)
    
    # feed option click 
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="gadgets"]/table/tbody/tr[18]/td[2]/a[2]/img'))).click()
    # driver.find_element_by_xpath('//*[@id="gadgets"]/table/tbody/tr[18]/td[2]/a[2]/img').click()
    
    # filling the link 
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="feedUrl"]'))).send_keys(feed_link)
    # driver.find_element_by_xpath('//*[@id="feedUrl"]').send_keys(feed_link)
    
    # continue 
    driver.find_element_by_id('save-button').click()

    
def login_to_medium_and_post(driver, data,  url = 'https://medium.com/'):
    wait = WebDriverWait(driver, 10)
    # intitiate the link 
    driver.get(url)
    time.sleep(5)
 
    frames = driver.find_elements(By.TAG_NAME, 'iframe')

    time.sleep(10)
    try:
        driver.switch_to.frame(frames[1])
        wait.until(EC.element_to_be_clickable((By.ID, 'continue-as'))).click()
        # driver.find_element_by_id('continue-as').click()
        print('logged into medium ...succesfully ')
        driver.switch_to.default_content()
         
    except Exception as e:
        # driver.refresh()
        sys.exit() 
    
    try:
        profile = wait.until(EC.presence_of_element_located((By.XPATH, 
                '//*[@id="root"]/div/nav/div/div/div/div/div[2]/div/div[5]/div/button/img')))
        # //*[@id="root"]/div/nav/div/div/div/div/div[2]/div/div[6]/div/button/img
        profile.click()
    except Exception as e:
        try:
            driver.find_element_by_xpath('//*[@id="root"]/div/nav/div/div/div/div/div[2]/div/div[6]/div/button/img').click()
        except Exception as e:
            print(e)
            driver.close()
            sys.exit() 

    frames = driver.find_elements(By.TAG_NAME, 'frame')
    
    try:    
        stories_button = wait.until(EC.presence_of_element_located((By.XPATH,
        '/html/body/div[3]/div/div/div/div[1]/div/ul/li[4]/h4/a')))    
        stories_button.click()
    except:
        try:
            stories_button = wait.until(EC.presence_of_element_located((By.XPATH, 
                            '/html/body/div[2]/div/div/div/div[1]/div/ul/li[4]/h4/a'))).click()
        except:
            driver.close()
            sys.exit()
    
    # driver.get('https://medium.com/me/stories/drafts')
    time.sleep(3)
    # lets get the data of all the posted content 
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/section/div[2]/ul/li[2]/h4'))).click()
    time.sleep(4)
 
    previous_content_titles = []
    previous_content_link = driver.current_url
    try:
        title_elements = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'h3')))
        i = 1
        for item in title_elements:
            if i%2 != 0:
                element = item.find_element_by_tag_name('a')
                string = element.text
                previous_content_titles.append(string.strip().lower())
                i = i + 1
            else:
                i = i + 1
        # print(previous_content_titles)
    except Exception as e:
        print(e) 
    
    print(' total previous content : ', len(previous_content_titles))  
    print('previous contents : ', previous_content_titles)
    import_button = wait.until(EC.presence_of_element_located((By.XPATH, 
                                    '//*[@id="root"]/div/section/div[1]/div/div')))
    import_button.click()
    import_url = driver.current_url
    
    links = []
    titles = []
    
    print(previous_content_titles[1] in data['titles'])
    
    for title, link in zip(data['titles'], data['links']):
        if title.strip().lower() not in previous_content_titles:
            titles.append(title)
            links.append(link)
            
    print(titles)
    print(len(titles))
    print(len(links))
    
    for link, title in zip(links, titles):
        driver.get(previous_content_link)
        time.sleep(5)
        previous_content_titles = []
        try:
            title_elements = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'h3')))
            i = 1
            for item in title_elements:
                if i%2 != 0:
                    element = item.find_element_by_tag_name('a')
                    string = element.text
                    previous_content_titles.append(string.strip().lower())
                    i = i + 1
                else:
                    
                    i = i + 1
            # print(previous_content_titles)
        except Exception as e:
            print(e)                 
            
        if title.strip().lower() not in previous_content_titles:
            
            time.sleep(5)
            driver.get(import_url)
            time.sleep(5)
            
            try:
                time.sleep(3)
                driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/button[1]').click()
                time.sleep(3)
                link_bar = wait.until(EC.presence_of_element_located((By.XPATH, '//*[starts-with(@id, "editor")]/p')))
                # link_bar = driver.find_element_by_xpath('//*[@id="editor_7"]/p')
                link_bar.send_keys(link)
                link_bar.send_keys(Keys.ENTER)
            except Exception as e:
                try:
                    link_bar = driver.find_element_by_xpath('//*[@id="editor_7"]/p')
                    link_bar.send_keys(link)
                    link_bar.send_keys(Keys.ENTER)
                except Exception as e:
                    driver.close()
                    sys.exit()
                
            time.sleep(5)
            try:
                see_your_story = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/button')))
                see_your_story.click()
            except Exception as e:
                driver.close()
                sys.exit()
            
            time.sleep(5)
            
            try:
                publish_button = driver.find_element_by_xpath('//*[starts-with(@id, "_obv.shell._surface")]/div/div[2]/div[2]/div[2]/div[1]/button/span') 
                publish_button.click()
            except:
                try:
                    publish_button = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[2]/div[2]/div[1]/button/span') 
                    publish_button.click()
                except:
                    driver.close()
                    sys.exit()
            
            time.sleep(8)
            
            
            try:
                driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div/button').click()
                time.sleep(6)
            except:
                pass 
            
            
            try:
                final_publish_button = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div/div/div[2]/div[6]/div[1]/div/button')))
                final_publish_button.click()
                time.sleep(5)
            except Exception as e:
                pass  
            
            try:
                continue_button = driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div/div[2]/div/button')
                continue_button.click()
            except Exception as e:
                pass
            
            try:
                time.sleep(5) 
                wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div/div/div[2]/div'))).click()
                time.sleep(5)
            except Exception as e:
                pass
                
            try:
                time.sleep(5)
                wait.until(EC.presence_of_element_located((By.XPATH, 
                            '/html/body/div[2]/div/div/div/div/div/div[2]/div/button'))).click()
            except Exception as e:
                print(e) 
                
            try:
                time.sleep(5)
                wait.until(EC.presence_of_element_located((By.XPATH, 
                            '/html/body/div[2]/div/div/div/div/div/div[2]/div'))).click()
                time.sleep(5)
            except Exception as e:
                print(e) 
            
        else:
             continue 
   
def main():
    url = 'https://startuptimes.net/articles'
    driver = create_driver(url)
    time.sleep(3)
    
    login_to_stackoverflow(driver)
    time.sleep(20)
    post_links = get_all_post_links(driver)
        
    print('extracting RSS FEED .... ')    
    rss_feed_link =  get_rss_feed(driver)
    print('RSS FEED extracted... ')
    
    time.sleep(5)
    login_to_medium_and_post(driver, post_links)

if __name__ == '__main__':
    main()