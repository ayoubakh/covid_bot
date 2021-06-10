from bs4 import BeautifulSoup as bs
import requests

def prepare_soup():
    hespress = requests.get("https://covid.hespress.com", headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0',
        })
    hespress.encoding = "utf-8"
    html_hespress = hespress.text
    return bs(html_hespress, features="html.parser")

def get_covid_stat(soup):    
    daily_test = soup.select("a[href='#daily_tests']")[1]
    new_cases_links = soup.select("a[href='#new_cases']")
    daily_new_cases = new_cases_links[0].span.text
    daily_recovered = new_cases_links[1].span.text
    daily_deaths = new_cases_links[2].span.text
    last_update = soup.select_one("#region_ma02").h6.text
    result = {
        "last_update": last_update,
        "daily_tests": daily_test.span.text,
        "daily_new_cases": daily_new_cases,
        "daily_recovered": daily_recovered,
        "daily_deaths": daily_deaths
    }
    return result

def get_covid_stat_allregions(soup) :
    result = {"last_update": soup.select_one("#region_ma02").h6.text}
    for i in range(1,13):

        region_id = "#region_ma{}".format("0" + str(i) if i < 10 else i)
        html_regions = soup.select("div{}".format(region_id))
        for region in html_regions:
            region_name = region.h5.text
            result[region_name] = []
            for city in region.table.find_all("tr"):
                data = {}
                data["city_name"] = city.th.text
                city_data = city.find_all("td")
                data["new_cases"] = city_data[0].text if city_data[0].text != "" else "0"
                data["deaths"] = city_data[1].text if city_data[1].text != "" else "0"
                
                city_name = city.th.text
                
                result[region_name].append(data)
                pass
            pass
    return result

def findby_city_name(regions: dict, city_name: str):
    for region in regions:
        if region == "last_update": continue
        for city in regions[region] :
            if city["city_name"] == city_name :
                city["last_update"] = regions["last_update"]
                return city
    return "سمح لينا، سمية المدينة ملقيناهاش."
    pass
