from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# FUNCTION AUTOMATICALLY LOGIN TO SHOPEE ACCOUNT

# [HOW ?] Replace the 'UserName' and 'Password' in the .send_keys("UserName/Password") in line 13, 16 by those of your account

def sp_login(driver):
    
        # Input the username:    
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div/div/div/div[2]/form/div/div[2]/div[2]/div[1]/input'))).send_keys("UserName")
        
        # Input the password:            
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div/div/div/div[2]/form/div/div[2]/div[3]/div[1]/input'))).send_keys("Password")

        # Login !
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div/div/div/div[2]/form/div/div[2]/div[3]/div[1]/input'))).send_keys(Keys.ENTER)
