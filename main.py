from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from info_card import price_taker
import time 

start = time.time()
# Timer start
start = time.time()


df = pd.DataFrame()

# Parameters
makes = ['Mitsubishi']
price_from_val = '17000'
price_to_val = '25000'
models_to_select = ['Pajero']
path_to_html = r"C:\Users\user\Desktop\Internship\Web_Scrapping\page.html"
path_to_adblockplus = r"C:\Users\user\Desktop\Internship\Web_Scrapping\extension_3_18_1_0.crx"

# Settings for Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_extension(path_to_adblockplus)

# Turning on Chrome with add-on
driver = webdriver.Chrome(options=chrome_options)

# Opening main page
driver.get("https://ru.turbo.az/")

car_data = []

for i in makes:
    # total = []
    # Получите список всех дескрипторов вкладок
    all_tabs = driver.window_handles

    # Переключитесь на первую вкладку
    driver.switch_to.window(all_tabs[0])
#-----------------------------------------------------------------------------------------------

    # Clicking on the dropddown of Makes
    dropdown = driver.find_element(By.CLASS_NAME, "tz-dropdown")
    dropdown.click()

    # Choosing make
    choose_make = driver.find_element(By.XPATH, f"//span[text()='{i}']")
    choose_make.click()
#-----------------------------------------------------------------------------------------------
    
    # 13.469862222671509

    # Откроем выпадающий список с моделями, если он скрыт
    dropdown_button = driver.find_element(By.CSS_SELECTOR, ".tz-dropdown[data-id='q_model']")
    if not dropdown_button.get_attribute('aria-expanded') == 'true':
        dropdown_button.click()

    # Соберите все доступные модели в словарь
    available_models = {model.text.strip(): model for model in driver.find_elements(By.CLASS_NAME, "tz-dropdown__option-label")}

    # Выберите модели из списка models_to_select
    for model_name in models_to_select:
        if model_name in available_models:
            available_models[model_name].click()

    
    
#-----------------------------------------------------------------------------------------------
    # Clicking on the Price from input
    price_from = driver.find_element(By.ID, "q_price_from")

    # Получить текущее значение элемента ввода
    current_value = price_from.get_attribute('value')

    # Проверить, есть ли значение в элементе ввода
    if current_value:
        print("Элемент ввода содержит значение:", current_value)
    else:
        print("Элемент ввода пуст.")
        price_from.send_keys(price_from_val)

#-----------------------------------------------------------------------------------------------
    # Clicking on the Price to input
    price_to = driver.find_element(By.ID, "q_price_to")

    # Получить текущее значение элемента ввода
    current_value = price_to.get_attribute('value')

    # Проверить, есть ли значение в элементе ввода
    if current_value:
        print("Элемент ввода содержит значение:", current_value)
    else:
        print("Элемент ввода пуст.")
        price_to.send_keys(price_to_val)

#-----------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------
    time.sleep(5)
    # Click on butten 'Показать результаты'
    show_results = driver.find_element(By.XPATH, f'//*[@id="new_q"]/div/div[4]/div[2]/button')
    show_results.click()

#-----------------------------------------------------------------------------------------------
    pages = 0
    while True:
        pages += 1
        # Save HTML of the current page
        page_html = driver.page_source

        with open('page.html', 'w', encoding='utf-8') as file:
            file.write(page_html)
        
        # Add the list of prices of one page to the global list of one make
        current_page_data = price_taker(path_to_html)
        
        # Add make to each car info
        for car_info in current_page_data:
            car_info['Make'] = i
            car_data.append(car_info)

        try:
            # Serch for reference on the next page
            next_link = driver.find_element(By.CSS_SELECTOR, 'a[rel="next"]')
            
            # If reference is found then continue
            # Else stop and enter next make
            next_link.click()
            print('PAGE DONE, GOING TO THE NEXT')
            print(pages)
            # print(total)
        except:
            print('BREAK')
            print(pages)
            # print(total)
            break
  
    print('MAKE DONE')
 

driver.quit()

# Creating DataFrame from the list of car data
df = pd.DataFrame(car_data)
df.rename(columns={
    'name': 'Model',
    'price': 'Price AZN',
    'year': 'Year',
    'liters': 'Volume L',
    'mileage': 'Mileage',
    'link': 'Link'
}, inplace=True)

# Convering currencies
def convert_currency(value):
    value_str = str(value)
    if '$' in value_str:
        return float(value_str.replace('$', '').replace(' ', '')) * 1.7
    elif '€' in value_str:
        return float(value_str.replace('€', '').replace(' ', '')) * 1.82
    elif 'AZN' in value_str:
        return float(value_str.replace('AZN', '').replace(' ', ''))
    else:
        return float(value_str.replace(' ', ''))

# Converting currencies for 'Price AZN' column
df['Price AZN'] = df['Price AZN'].apply(convert_currency)

df['Median Price'] = df['Price AZN'].median()
df['Median Mileage'] = df['Mileage'].median()
df['Median Year'] = df['Year'].median()

# Exporting as XLSX
df.to_excel('Makes.xlsx', index=False)
print(df)

# Time of script work
end = time.time() - start
print(end)