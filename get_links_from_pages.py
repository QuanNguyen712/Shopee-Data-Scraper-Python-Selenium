from selenium import webdriver
from selenium.webdriver.common.by import By
from queue import Queue
from time import sleep
from func_login import sp_login
import pandas as pd
import threading

#============================================================================
    # DECLARE VARIABLES:
global link_list
link_list = [] # List stores all product links accross pages
get_link_thread_list = [] # List store executing threads for the later join
page_queue = Queue() # Queue store page index from 0 to 16
[page_queue.put(i) for i in range(17)] # Store 0 to 16 integers into the Queue

#============================================================================
    # FUNCTION ACCESSES THE PRODUCT PAGE AND GET ALL PRODUCT LINKS
    
    # [HOW ?] Drivers (threads) sequentially get the page index from 'page_queue' ... 
    # ... to get all the product links until passing through all the pages, which means until the 'page_queue' is empty
    
def get_link_Worker(get_link_driver): 
    while page_queue.qsize() != 0:
        # Access the product page, login and zoom out for the total visibility
        page_num = page_queue.get()
        get_link_driver.get("https://shopee.vn/search?keyword=dung%20d%E1%BB%8Bch%20v%E1%BB%87%20sinh%20nam&page={}".format(page_num))
        sleep(7)
        try:
            sp_login(get_link_driver)
        except:
            pass
        sleep(7)
        get_link_driver.execute_script("document.body.style.zoom='10%'")
        sleep(10)
        
        # Identify and append every single product link on the page to the 'link_list'
        for item_num in range(1, len(get_link_driver.find_elements(By.CLASS_NAME, 'col-xs-2-4.shopee-search-item-result__item'))+1):
            link_list.append(get_link_driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[2]/section[2]/ul/li[{}]/a'.format(item_num)).get_attribute('href'))

#============================================================================
    # MAIN THREAD EXECUTION
# Open simultaneously working drivers (threads) (4 is recommended)
get_link_drivers = [webdriver.Chrome() for driver in range(4)]

# Each driver (thread) execute the targeted function to access the page link and get all product links,...
# ... once the task is done, it would get the first-standing page index at that time in the 'page_queue' and repeat.
for driver in get_link_drivers:
    t = threading.Thread(target=get_link_Worker, args=(driver,))
    get_link_thread_list.append(t)
    t.start()

# Join all the working threads
# This step make '# OUTPUT THE RESULT' step to wait until all product links are gotten ...
# ... without this step, the '# OUTPUT THE RESULT' lines of code would be executed before all product links are stored into the 'link_list' 
for thread in get_link_thread_list:
    thread.join()
    
# ============================================================================  
    # OUTPUT THE RESULT
# Change the desired directory into the .to_excel() 
pd.DataFrame({'Total Link': link_list}).to_excel(r"C:\Users\Admin\Desktop\TotalLinkNew.xlsx", sheet_name='Data', index=False)
print('{} product links were found'.format(len(link_list)))
