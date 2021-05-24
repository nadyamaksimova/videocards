from bs4 import BeautifulSoup as bs
import requests as req
import linker
from fake_useragent import UserAgent
from price import min_price_handler, max_price_handler


class Parser2:
    link = str()
    tovar = str()

    def __init__(self, link):
        self.link = link
        self.tovar = link

    def avito(self):
        link = linker.avito(self.link)
        d = {}
        parsed = bs(self.get_resp(link), "html.parser")
        pars = parsed.find_all("div", class_="iva-item-titleStep-2bjuh")
        prices = parsed.find_all("div", class_="iva-item-priceStep-2qRpg")
        i = 0
        for p in pars:
            if p.text.lower().__contains__(self.tovar.lower()):
                d[p.text] = ["https://www.avito.ru/" + p.find("a").get("href"),
                             prices[i].text.translate({ord(i): None for i in "\0₽"})]
                i += 1
        return d

    def citilink(self):
        link = linker.citi(self.link)
        d = {}
        parsed = bs(self.get_resp(link), "html.parser")
        pars = parsed.find_all("div", class_="ProductCardVerticalLayout ProductCardVertical__layout")
        i = 0
        for p in pars:
            if p.text.lower().__contains__(self.tovar.lower()):
                #if p.text.__contains__("Узнать о поступлении"):
                 #   continue
                pp = p.find("div", class_="ProductCardVertical__description").find("a",
                                                                                   class_="ProductCardVertical__name")
                d[pp.text] = ["https://www.citilink.ru/" + pp.get("href"),
                              p.find_all("span", class_="ProductCardVerticalPrice__price-current_current-price")[
                                  0].text.strip()]
                i += 1
        return d

    def dns(self, tt=""):
        link = linker.dns(self.link, tt)
        d = {}
        parsed = bs(self.get_resp(link), "html.parser")
        pars = parsed.find_all("div", class_="catalog-product ui-button-widget")
        print(parsed.find_all("span", id = "as-l4SM-I"))
        for p in pars:
            temp = p.find("a", class_="catalog-product__name ui-link ui-link_black")
            photo = p.find("div", class_="catalog-product__image")
            d[temp.text] = ["https://www.dns-shop.ru/" + str(temp.get("href"))+"?price="+min_price_handler(min_price)+"-"+max_price_handler(max_price),""]
        return d

    def get_resp(self, link):
        ua = UserAgent()
        resp = req.get(link, headers={'User-Agent': ua.chrome})
        return resp.text
