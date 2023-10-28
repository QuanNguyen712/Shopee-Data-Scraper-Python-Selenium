from selenium import webdriver
from func_login import sp_login
from func_target_product_info import sp_scraper
from selenium.webdriver.common.by import By
from queue import Queue
from time import sleep
import pandas as pd
import threading

# ============================================================================      
    # DECLARE VARIABLES:
global link_sequence, out_df
link_sequence = Queue()
out_df = pd.DataFrame(columns=['Info', 'Title', 'Sales', 'Price', 'Vendor', 'Vendor Link', 'Rating Star', 'Rating Star Dis', 'Voucher', 'Link'])
thread_list = []
link_list_back_up = []
# Store all gotten product links into a Queue- 'link_sequence'
[link_sequence.put(link) for link in list(pd.read_excel(r"C:\Users\Admin\Desktop\TotalLink.xlsx", sheet_name='Data')['Total Link'])]

# ============================================================================
    # FUNCTION ACCESSES THE PRODUCT LINK AND GET INFORMATION
    
    # [HOW ?] Drivers (threads) sequentially get the product link from 'link_sequence' ... 
    # ... and scrape information until the last link, which means until the 'link_sequence' is empty

def Worker(working_driver):
    while link_sequence.qsize() != 0:
        
        # Access the product link, login and zoom out for the total visibility
        product_link = link_sequence.get()
        working_driver.get(product_link)
        sleep(6)
        try:
            sp_login(working_driver)
        except:
            pass
        sleep(6)
        working_driver.execute_script("document.body.style.zoom='10%'")
        sleep(6)
        
        # Product variation check:
        # Some product has multiple fragrance/ variation with different prices,... 
        # ... Thus, the following step automatically clicks on each fragrance for the price of the clicked...
        # ... variation to be visible, then accurately scrapes information of that product variation
        # ... To annotated the information is of the variation, the 'var_' prefix is added to the 'Detail' 
        fragrance = working_driver.find_elements(By.CLASS_NAME, 'product-variation')
        if len(fragrance) == 0:
            print('no product var')
            out_list = sp_scraper(working_driver)
            out_list.append(product_link)
            out_df.loc[len(out_df.index)] = out_list     
        else:
            try:
                for product_var_idx in range(len(fragrance)):
                    product_var_info_list = []
                    
                    working_driver.execute_script("fragrance = document.getElementsByClassName('product-variation');")    
                    working_driver.execute_script("fragrance[{}].click();".format(product_var_idx))
                    sleep(1)
                    
                    out_list = sp_scraper(working_driver)
                    out_list.append(product_link)                        
                    product_var_info_list = out_list
                    product_var_info_list[0] = 'var_'+ fragrance[product_var_idx].text + '_' + product_var_info_list[0]
                    out_df.loc[len(out_df.index)] = product_var_info_list
            except:
                print('product var was missing')
                pass  

# ============================================================================      
    # MAIN THREAD EXECUTION
# Open simultaneously working drivers (threads) (3 is recommended)
working_drivers = [webdriver.Chrome() for driver in range(3)]

# Each driver (thread) execute the targeted function to access the product link and get all information,...
# ... once the task is done, it would get the first-standing link at that time in the 'page_queue' and repeat.
for driver in working_drivers:
    t = threading.Thread(target=Worker, args=(driver,))
    thread_list.append(t)
    t.start()
    
# Join all the working threads
# This step make the code from '# WRAP UP !!!' and 'OUTPUT THE RESULT' wait until all product information are gotten ...
# ... without this step, the below code of the main thread would be executed before all product links are accessed to get information.
for thread in thread_list:
    thread.join()

# ============================================================================
    # WRAP UP !!!
# This step would back-up in case the working threads are disupted due to error such as internet connection unstability ...
# Specifically, when error occurs, all remaining product links which have not been accessed to scrape information...
# ... would be stored into a xlsx. file for ultilizing in the re-run of the code to continuously scrape information instead of ...
# ... starting from the begining of the 'link_sequence', which is the waste of time.
if link_sequence.qsize() == 0:
    print('Scrapt Done')
else:
    print('Something is wrong')
    for _ in range(link_sequence.qsize()):
        link_list_back_up.append(link_sequence.get())    
    pd.DataFrame({'Remaining Link': link_list_back_up}).to_excel(r"C:\Users\Admin\Desktop\'Remaining_Link'.xlsx", sheet_name='Data', index=False)

# ============================================================================  
    # OUTPUT THE RESULT
# Change the desired directory into the .to_excel() 
out_df.to_excel(r"C:\Users\Admin\Desktop\OutPutProductInfo.xlsx", sheet_name='Data', index=False)
