import requests
from bs4 import BeautifulSoup
from time import sleep

def check(element,slice):
    return element.text[slice:] if element else "Отсутствует информация"

def check_1(element):
    return element.text if element else "Отсутствует информация"

def get_product_links(search):
    total = total_pages(search)
    base_url = 'https://obuv-tut2000.ru/magazin/search?gr_smart_search=1&search_text='

    for page in range(1, total + 1):
        if page == 1:
            url = base_url + search
        else:
            url = f"{base_url}&page={page}"

        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        data = soup.find_all("div", class_="product-item__top")

        for item in data:
            link_tag = item.find("a")
            if link_tag:
                yield "https://obuv-tut2000.ru" + link_tag.get("href")
        sleep(1)

def total_pages(search):
    base_url = 'https://obuv-tut2000.ru/magazin/search?gr_smart_search=1&search_text='
    url = base_url + search
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    last_page_li = soup.find("li", class_="page-num page_last")
    if last_page_li:
        href = last_page_li.find("a").get("href")
        try:
            page_number = int(href.split("p=")[-1].split("&")[0])
        except:
            page_number = 1
        return page_number
    else:
        return 1

search=input()

for card_url in get_product_links(search):
    sleep(3)
    response = requests.get(card_url)
    soup_1 = BeautifulSoup(response.text, "lxml")
    data = soup_1.find("div", class_="card-page")

    name = check_1(data.find("h1"))

    shoe_type = name.split()[0] if name != "Отсутствует информация" else "Неизвестно"

    article_element = data.find("div", class_="shop2-product-article")
    article = check(article_element, 9)

    price = check_1(data.find("strong"))

    country = check_1(data.find("div", class_="gr-vendor-block")).strip()

    color_element = data.find("div", class_="option-item cvet odd")
    color = check(color_element, 4)

    material_element = data.find("div", class_="option-item material_verha_960 odd")
    upper_material = check(material_element, 14)

    size_element = data.find("div", class_="option-item razmery_v_korobke even")
    size = check(size_element, 7)

    season_element = data.find("div", class_="option-item sezon even")
    season = check(season_element, 5)

    print(article)
    print(name)
    print(shoe_type)
    print(season)
    print(price)
    print(size)
    print(upper_material)
    print(color)
    print(country, "\n")
