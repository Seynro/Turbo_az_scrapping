from bs4 import BeautifulSoup

def price_taker(path_to_html):
    car_info_list = []
    base_url = "https://ru.turbo.az"

    # Reading downloaded HTML
    with open(path_to_html, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Creating object BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find element with class "section-title_name" and that contains "ОБЪЯВЛЕНИЯ"
    section_title = soup.find('p', class_='section-title_name', text='ОБЪЯВЛЕНИЯ')

    # Find all next element of class "products-i"
    ads_elements = section_title.find_all_next('div', class_='products-i')

    # Loop through the ad elements to extract and format the required information
    for ad in ads_elements:
        car_info = {}
        
        # Extracting name
        name_tag = ad.find('div', class_='products-i__name')
        car_info['name'] = name_tag.text.strip() if name_tag else None

        # Extracting price (keeping as a string)
        price_tag = ad.find('div', class_='product-price')
        car_info['price'] = price_tag.text.strip() if price_tag else None

        # Extracting car link and adding base URL
        link_tag = ad.find('a', class_='products-i__link')
        car_info['link'] = base_url + link_tag['href'] if link_tag else None

        # Extracting attributes (year, liters, mileage)
        attributes_tag = ad.find('div', class_='products-i__attributes')
        if attributes_tag:
            attributes = attributes_tag.text.strip().split(', ')
            car_info['year'] = int(attributes[0]) if len(attributes) > 0 else None
            car_info['liters'] = float(attributes[1].replace(' л', '')) if len(attributes) > 1 else None
            car_info['mileage'] = int(attributes[2].replace(' км', '').replace(' ', '')) if len(attributes) > 2 else None

        # Adding to existing list
        car_info_list.append(car_info)
        print(f"Processing {len(car_info_list)} cars from {path_to_html}")


    return car_info_list
