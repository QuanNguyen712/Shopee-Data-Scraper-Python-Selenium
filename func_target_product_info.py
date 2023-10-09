from selenium.webdriver.common.by import By


def sp_scraper(driver):
    # FUNCTION SCRAPES INFORMATION IN THE PRODUCT PAGE:
        
    # [HOW ?] After inspecting Shopee product link, the targeted product information is located in the...
    # ... respective classes as stated below. The function returns 'output_list' which contains...
    # ... sequentially crawled information of the product.
    
    output_list = []
    
        # 1. Product Detail:
    
    product_detail_elem = driver.find_element(By.CLASS_NAME, 'MCCLkq')
    product_detail = product_detail_elem.text
    output_list.append(product_detail)
    
        # 2. Product Title:
    
    product_title_elem = driver.find_element(By.CLASS_NAME, '_44qnta')
    product_title = product_title_elem.text
    output_list.append(product_title)       
    
        # 3. Sales:
    sales_elem = driver.find_element(By.CLASS_NAME, 'e9sAa2')
    sales = sales_elem.text
    output_list.append(sales)
    
        # 4. Price:
    price_elem = driver.find_element(By.CLASS_NAME, 'pqTWkA')
    price = price_elem.text
    output_list.append(price)
        
        # 5. Vendor:
    vendor_elem = driver.find_element(By.CLASS_NAME, 'VlDReK')
    vendor = vendor_elem.text
    output_list.append(vendor)

        # 6. Vendor Link:
    vendor_link_elem = driver.find_element(By.CLASS_NAME, 'W0LQye')
    vendor_link = vendor_link_elem.get_attribute('href')
    output_list.append(vendor_link)    
    
        # 7. Rating Star:            
    rating_star_elem = driver.find_elements(By.CLASS_NAME, '_1k47d8')
    rating_star = [rating_star.text for rating_star in rating_star_elem]
    output_list.append(rating_star)
    
        # 8. Rating Star Distribution:
    rating_star_distribution_elem = driver.find_element(By.CLASS_NAME, 'product-rating-overview__filters')
    rating_star_distribution = rating_star_distribution_elem.text
    output_list.append(rating_star_distribution)
    
        # 9. Vendor Voucher:
    # The 'try' and 'except' are applied as some products do not have incentives  
    try:
        shop_voucher_elem = driver.find_element(By.CLASS_NAME, 'product-shop-vouchers__list')
        shop_voucher = shop_voucher_elem.text
        output_list.append(shop_voucher)
    except:
        output_list.append('No Voucher')
    
    return output_list
