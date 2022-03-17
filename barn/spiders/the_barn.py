from unicodedata import category
import scrapy
import json
from ..items import BarnItem


class ExampleSpider(scrapy.Spider):
    name = 'barn'
    allowed_domains = ['www.thebarn.net.au/']
    start_urls = ['https://www.thebarn.net.au/']
    main_url = "https://www.thebarn.net.au"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
    
    def parse(self, response):
        
        
        cat1 = response.xpath('//div[contains(@class,"row")]//@href').extract()
        count  = 0
        c = 0
        for cat in cat1:
            print(len(cat1),"-------------cat1--------------")
            c += 1
            count += 1
            if cat == "#":
                count = 0
                continue
            if count == 1:
                continue
        
            gun_url =  self.main_url + cat

            print("\n {c}. Processing URL: {gun_url}".format(c = c,gun_url=gun_url))
            req = scrapy.Request(gun_url , callback=self.parse_data, headers = self.headers, dont_filter=True)
    
            yield req
            break
            
            
    def parse_data(self, response):
        
        urls = response.xpath('//div[@class="subcategories-grid"]//@href').extract()
        if len(urls)>0:
            # print("--------------in if-------------")
            # i = 0
            for url in urls:
                # print(url,"*******************url----------------------------")
                # i += 1
                req = scrapy.Request(self.main_url + url , callback=self.parse_data, headers = self.headers, dont_filter=True)
                yield req
                break
            
        else:
            
            category3 = response.url.split("/")[-2]
            try:
                category1 = response.xpath('//div[@class="col-xs-12"]/span/a[2]//text()').extract()[0]
            except:
                category1 = ""
            try:
                category2 = response.xpath('//div[@class="col-xs-12"]/span/a[3]//text()').extract()[0]
            except:
                category2 = category3
                category3 = ""

            temp = response.url.split("/")[-1]
            
            if category2 == "":
                category
            # print(response.url,"**************---------response url--------------")
            gun_url = "https://www.thebarn.net.au/handlers/productshandler.ashx?action=search"
            payload = {
            'CategoryID': temp,
            'Keywords': "",
            'SortOrder': 'productname asc',
            'MinPrice': "0",
            'MaxPrice': "0",
            'Ago': "0"
        }

            r = scrapy.FormRequest(gun_url,formdata=payload,dont_filter=True,callback=self.parse_fun)
            r.meta["category1"] = category1
            r.meta["category2"] = category2
            r.meta["category3"] = category3
            
            yield r

    def parse_fun(self,response):
        # print("**************in parse fun*********" )
        items = BarnItem()
        category1 = response.meta["category1"]
        category2 = response.meta["category2"]
        category3 = response.meta["category3"]
        
        b = json.loads(response.text)
        try:
            product_id = b["Products"][0]["Product"]["Id"]
        except:
            product_id = ""
        
        try:
            product_title = b["Products"][0]["Product"]["ProductTitle"]
            t = product_title.split(" ")
            url = "https://www.thebarn.net.au/Products/"
            for i in range(len(t) - 1):
                url = url + t[i] + "%20"
            url = url + t[-1] + "/" + str(product_id)
        except: 
            product_title = ""
            url = ""
        try:
            product_code =b["Products"][0]["Product"]["ProductCode"]
        except:
            product_code = None
        if product_code is None:
            product_code = product_id
        # print(product_code,"------code-----------")

        try:
            product_Description = b["Products"][0]["Product"]["ProductDescription"]
        except:
            product_Description = ""
        try:
            product_price = b["Products"][0]["Prices"]["RegularPrice"]
        except:
            product_price = ""
        
        items['category1'] = category1
        items['category2'] = category2
        items['category3'] = category3
        items["id"] = product_id
        items['product_code'] = product_code
        items['title'] = product_title
        items['description'] = product_Description
        items['product_url'] = url
        items['price'] = product_price

        
        
        yield items

    



