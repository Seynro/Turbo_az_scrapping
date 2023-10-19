from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time 

make = 'bmw'
model = 'x5'
from_year = 2020
to_year = 2024
path_to_html = r"C:\Users\user\Desktop\Internship\Web_Scrapping\page.html"

def price_bidfax(path_to_html):
    car_info_list = []
    base_url = "https://ru.turbo.az"

    # Reading downloaded HTML
    with open(path_to_html, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Creating object BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find element with class "section-title_name" and that contains "ОБЪЯВЛЕНИЯ"
    # Extracting information for all cars on the page and saving it in a list of dictionaries
    cars_data = []

    # Loop through all 'caption' divs, each representing a car
    for caption_div in soup.find_all('div', class_='caption'):
        car_info = {}
        
        h2_text = caption_div.find('h2').text.strip()
        details_list = h2_text.split()
        
        # Найдем индекс года
        year_index = [i for i, s in enumerate(details_list) if s.isdigit() and len(s) == 4][0]

        car_info["year"] = details_list[year_index]
        car_info["brand"] = details_list[0]
        car_info["model"] = " ".join(details_list[1:year_index])

        # Проверяем наличие цвета в названии
        if "L" in details_list[year_index + 3]:  # Если следующий после года элемент это объем двигателя, то цвета нет
            engine_index = year_index + 3
        else:  # Иначе цвет есть
            engine_index = year_index + 2

        car_info["engine_info"] = details_list[engine_index]

        car_info["condition"] = caption_div.find('p', class_='short-story2').find('span').text.strip()
        car_info["damage"] = caption_div.find_all('p', class_='short-story')[1].find('span').text.strip()
        car_info["mileage"] = caption_div.find_all('p', class_='short-story2')[1].find('span').text.strip()
        car_info["vin"] = details_list[-1]
        car_info["link"] = caption_div.find('a')['href']
        
        cars_data.append(car_info)

    return cars_data



def bidfax(make, model, from_year, to_year, path_to_html):
    # url = f'https://en.bidfax.info/{make}/{model}/f/from-year={from_year}/to-year={to_year}/'
    cars_result = []

    pages = 1
    
    final_df = pd.DataFrame()
    while pages <= 1:
        url = f'https://en.bidfax.info/{make}/{model}/f/from-year={from_year}/to-year={to_year}/page/{pages}'
        # Settings for Chrome
        chrome = webdriver.ChromeOptions()
        # Turning on Chrome with add-on
        driver = webdriver.Chrome(chrome)
        # Opening main page
        driver.get(url)

        pages += 1
        # Save HTML of the current page
        page_html = driver.page_source

        with open('page.html', 'w', encoding='utf-8') as file:
            file.write(page_html)

        cars_bidfax = price_bidfax(path_to_html)

        cars_result.append(cars_bidfax)
        # time.sleep(10)
        # next_page = driver.find_element(By.CSS_SELECTOR, '#bottom-nav > div > span.pnext')
        # next_page.click()
        # Convert the list of dictionaries to a DataFrame
        current_df = pd.DataFrame(cars_bidfax)
        
        # Append the current DataFrame to the final DataFrame
        final_df = final_df.append(current_df, ignore_index=True)

        driver.quit()

        
#-----------------------------------------------------------------------------------------------
    # time.sleep(10)
    

    return final_df

result = bidfax(make,model,from_year, to_year, path_to_html)

print(result)

result.to_excel('BidFax.xlsx', index=False)
