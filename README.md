# Shopee-Data-Scraper-Python-Selenium

**Motivation:**

One day you decide to launch a Shopee vendor selling intimate washing for men and come up with different questions such as: How many vendors are there to compete? What are they currently offering? How are the sales? How my pricing should be to stand out among the crowd, etc.

It would be a nightmare scanning and scrolling across items and pages to manually check out the existing products.

Here Python Selenium come to the recuse !

**Prerequisite:**

Prepare at least 1 Shopee account and fill the ‘User Name’ and ‘Password’ into the ‘func_login’ before running the main code as Shopee requires a login in several phases along the scrapping. Multiple back-up accounts are recommended due to the anti- bot system of the platform.

**How does it work?**

For the keyword ‘dung dịch vệ sinh nam’ Shopee returns 17 pages with 60 (+/- 1) products per page. The code’s operation is broken-down into steps/ sub-steps as follow:

*I.	Collect all product links in 17 pages and store them into a list- ‘link_list’:*
1.	Open a browser(s) (Chrome driver).
2.	Access the first product page link via the opened browser(s).
3.	Login to Shopee (Shopee requires).
4.	Zoom out for the total visibility (Selenium is only able to scrape visible items).
5.	Get all product links on the current page and append to the ‘link_list’.
6.	Repeat step I.2 with the next product page link until all product links in the 17 pages are stored into the ‘link_list’.

*II.	From each link in the ‘link_list’ returned from step I, collect product information and store them into a DataFrame- ‘out_df’:*
1.	Open a browser(s) (Chrome driver).
2.	Access the first product link via the opened browser(s).
3.	Login to Shopee (Shopee requires).
4.	Zoom out for the total visibility (Selenium is only able to scrape visible items).
5.	Get all information on the current product page and append to the ‘out_df’.
6.	Repeat step II.2 with the next product link until information of all products in the ‘link_list’ is stored into the ‘out_df’.
