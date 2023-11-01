import asyncio
import math
from typing import KeysView
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


options = webdriver.ChromeOptions()

options.add_argument("start-maximized")


#options.add_argument("--headless=new")

options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")
options.add_argument("disable-notifications")
driver = webdriver.Chrome(options)


#driver.minimize_window()






#driver.implicitly_wait(10)


driver.get("https://proxyscrape.com/free-proxy-list")
time.sleep(3)

print(driver.find_element(By.CSS_SELECTOR, ".selectors .nice-select:nth-of-type(2)").tag_name)

driver.find_element(By.CSS_SELECTOR, "ul.list.httpanonimity > li[data-value=elite]")

#driver.find_element(By.ID, "sharehttp").get_attribute("href")
proxy_scrape_http_proxy_list_link = "https://api.proxyscrape.com/v2/?request=share&protocol=http&timeout=10000&country=all&ssl=all&anonymity=elite&simplified=true"

proxy_scrape_sharesocks4_proxy_list_link = driver.find_element(By.ID, "sharesocks4").get_attribute("href")

proxy_scrape_sharesocks5_proxy_list_link = driver.find_element(By.ID, "sharesocks5").get_attribute("href")



driver.get(proxy_scrape_http_proxy_list_link)
time.sleep(3)

proxy_scrape_http_proxy_list = driver.find_element(By.ID, "proxyshare").text.strip()

proxy_scrape_http_proxy_list = proxy_scrape_http_proxy_list.split()

proxy_scrape_http_proxy_list = list(set(proxy_scrape_http_proxy_list))

proxy_scrape_http_proxy_list = "\n".join(proxy_scrape_http_proxy_list) 


driver.get(proxy_scrape_sharesocks4_proxy_list_link)
time.sleep(3)
proxy_scrape_sharesocks4_proxy_list = driver.find_element(By.ID, "proxyshare").text.strip()

proxy_scrape_sharesocks4_proxy_list = proxy_scrape_sharesocks4_proxy_list.split()

proxy_scrape_sharesocks4_proxy_list = list(set(proxy_scrape_sharesocks4_proxy_list))

proxy_scrape_sharesocks4_proxy_list = "\n".join(proxy_scrape_sharesocks4_proxy_list) 


driver.get(proxy_scrape_sharesocks5_proxy_list_link)
time.sleep(3)

proxy_scrape_sharesocks5_proxy_list = driver.find_element(By.ID, "proxyshare").text.strip()

proxy_scrape_sharesocks5_proxy_list = proxy_scrape_sharesocks5_proxy_list.split()

proxy_scrape_sharesocks5_proxy_list = list(set(proxy_scrape_sharesocks5_proxy_list))

proxy_scrape_sharesocks5_proxy_list = "\n".join(proxy_scrape_sharesocks5_proxy_list)


proxy_scraper_mixed_proxy_list = proxy_scrape_http_proxy_list + "\n"+ proxy_scrape_sharesocks4_proxy_list +"\n"+ proxy_scrape_sharesocks5_proxy_list


print(proxy_scraper_mixed_proxy_list)

print(len(proxy_scraper_mixed_proxy_list))








driver.get("https://free-proxy-list.net/")

time.sleep(1)



free_proxy_list_ip_port_number = []
proxy_count = len(driver.find_elements(By.CSS_SELECTOR, "#list table:first-of-type tbody tr"))
print(proxy_count)

for x in range(proxy_count):

    free_proxy_list_ip = driver.find_elements(By.CSS_SELECTOR, "table:first-of-type tbody td:first-child")[x].text.strip()

    free_proxy_list_port_number = driver.find_elements(By.CSS_SELECTOR, "table:first-of-type tbody td:nth-child(2)")[x].text.strip()
    
    free_proxy_list_anonymity = driver.find_elements(By.CSS_SELECTOR, "table:first-of-type tbody td:nth-child(5)")[x].text.strip()

    if free_proxy_list_anonymity == "elite proxy" or "anonymous" and free_proxy_list_anonymity != "transparent":

        free_proxy_list_ip_port_number.append(free_proxy_list_ip.strip() + ":" + free_proxy_list_port_number.strip())
    else:
        continue


free_proxy_list_ip_port_number = list(set(free_proxy_list_ip_port_number))

print("********************************")
print(free_proxy_list_ip_port_number)
print(len(free_proxy_list_ip_port_number))

free_proxy_list_ips_port_number = "\n".join(free_proxy_list_ip_port_number)











driver.get("https://www.socks-proxy.net/")

time.sleep(1)


free_socks_proxy_list_ips_port_number = []


proxy_count = len(driver.find_elements(By.CSS_SELECTOR, "#list table:first-of-type tbody tr"))
print(proxy_count)

for x in range(proxy_count):

    free_proxy_list_ip = free_proxy_list_ip = driver.find_elements(By.CSS_SELECTOR, "table:first-of-type tbody td:first-child")[x].text.strip()

    free_proxy_list_port_number = driver.find_elements(By.CSS_SELECTOR, "table:first-of-type tbody td:nth-child(2)")[x].text.strip()
    
    free_proxy_list_anonymity = driver.find_elements(By.CSS_SELECTOR, "table:first-of-type tbody td:nth-child(6)")[x].text.strip()

    if free_proxy_list_anonymity == "elite proxy" or "anonymous" and free_proxy_list_anonymity != "transparent":

        free_socks_proxy_list_ips_port_number.append(free_proxy_list_ip.strip() + ":" + free_proxy_list_port_number.strip())
    else:
        continue



print("********************************")
print(free_socks_proxy_list_ips_port_number)
print(len(free_socks_proxy_list_ips_port_number))

free_socks_proxy_list_ips_port_number = list(set(free_socks_proxy_list_ips_port_number))

free_socks_proxy_list_ips_port_number = "\n".join(free_socks_proxy_list_ips_port_number)





















proxy_list_download_ips_ports_number = []

proxy_list_download_urls = ["https://www.proxy-list.download/HTTPS",
                            "https://www.proxy-list.download/HTTP",
                            "https://www.proxy-list.download/SOCKS5"]







for x in range(len(proxy_list_download_urls)):

    driver.get(proxy_list_download_urls[x])
    time.sleep(3)

    total_page_number = int(driver.find_element(By.CSS_SELECTOR, "#tpagess").text.split()[-1])
    print(total_page_number)

    

    for y in range(total_page_number):

        time.sleep(1)
        proxy_count = len(driver.find_elements(By.CSS_SELECTOR, "#example1 #tabli tr"))
    
        print(proxy_count)

        if(proxy_count == 0):
            break

        for z in range(proxy_count):

            proxy_list_download_https_ip = driver.find_elements(By.CSS_SELECTOR, "#example1 #tabli tr td:nth-child(1)")[z].text

            proxy_list_download_https_port = driver.find_elements(By.CSS_SELECTOR, "#example1 #tabli tr td:nth-child(2)")[z].text

            proxy_list_download_https_anonymity = driver.find_elements(By.CSS_SELECTOR, "#example1 #tabli tr td:nth-child(3)")[z].text

            if proxy_list_download_https_anonymity == "Elite" or "Anonymous" and proxy_list_download_https_anonymity != "Transparent":

                proxy_list_download_ips_ports_number.append(proxy_list_download_https_ip + ":" + proxy_list_download_https_port)
            else:
                continue


        print(proxy_list_download_ips_ports_number)

        proxy_list_download_ips_ports_number = list(set(proxy_list_download_ips_ports_number))
     
        print("*************")

        next_button = driver.find_element(By.CSS_SELECTOR, ".dataTables_paginate #example1_next button")
    
        ActionChains(driver).click(next_button).perform()
        
        


proxy_list_download_ips_ports_number = "\n".join(proxy_list_download_ips_ports_number)






free_proxy_world_ips_ports_number = []
free_proxy_world_page_number = 1
free_proxy_world_url = "https://www.freeproxy.world/?type=&anonymity=4&country=&speed=&port=&page={p}".format(p = free_proxy_world_page_number)


driver.get(free_proxy_world_url)
time.sleep(3)

free_proxy_world_total_proxy_count = int(driver.find_element(By.XPATH, '//*[@id="layui-laypage-1"]/span[1]').text.split()[-1])



free_proxy_world_total_page_count = math.ceil(free_proxy_world_total_proxy_count / 50)



for x in range(free_proxy_world_total_page_count):

    free_proxy_world_proxy_list = driver.find_elements(By.CSS_SELECTOR, "table tr:nth-child(2n)")

    free_proxy_world_ip_list = driver.find_elements(By.CSS_SELECTOR, "table tr:nth-child(2n) td:first-child")
    free_proxy_world_port_list = driver.find_elements(By.CSS_SELECTOR, "table tr:nth-child(2n) td:nth-child(2) a")

    print(len(free_proxy_world_ip_list))
    print(len(free_proxy_world_port_list))

    for y in range(len(free_proxy_world_proxy_list)):

        free_proxy_world_ip = free_proxy_world_ip_list[y].text.strip()
      
        free_proxy_world_port_number = free_proxy_world_port_list[y].text.strip()

        free_proxy_world_ips_ports_number.append(free_proxy_world_ip + ":" + free_proxy_world_port_number)


    free_proxy_world_page_number +=1

 
    driver.get("https://www.freeproxy.world/?type=&anonymity=4&country=&speed=&port=&page={p}".format(p = free_proxy_world_page_number))
    time.sleep(3)


free_proxy_world_ips_ports_number = list(set(free_proxy_world_ips_ports_number))


free_proxy_world_ips_ports_number = "\n".join(free_proxy_world_ips_ports_number)
print(free_proxy_world_ips_ports_number)
     
print("*************")









open_proxy_space_ips_ports_number = []

open_proxy_space_list_download_urls = ["https://openproxy.space/list/http",
                            "https://openproxy.space/list/socks4",
                            "https://openproxy.space/list/socks5"]



for x in range(len(open_proxy_space_list_download_urls)):

    driver.get(open_proxy_space_list_download_urls[x])

    time.sleep(3)

    proxy_list_text_area = driver.find_element(By.CSS_SELECTOR,"section.data textarea").text

    
    open_proxy_space_ips_ports_number = list(set(map(lambda x : x.strip() ,proxy_list_text_area.split())))

    


open_proxy_space_ips_ports_number = "\n".join(open_proxy_space_ips_ports_number)
print(open_proxy_space_ips_ports_number)




#proxy_list = "\n".join(proxy_list_download_ips_ports_number)

proxy_list = proxy_scraper_mixed_proxy_list +"\n"+ free_proxy_list_ips_port_number +"\n"+ free_socks_proxy_list_ips_port_number +"\n"+ proxy_list_download_ips_ports_number + "\n" + free_proxy_world_ips_ports_number + "\n" + open_proxy_space_ips_ports_number



with open("unchecked_proxy_list.txt", "w") as f:

    f.write(proxy_list)


driver.close()

#time.sleep(3)
#driver.implicitly_wait(10)


