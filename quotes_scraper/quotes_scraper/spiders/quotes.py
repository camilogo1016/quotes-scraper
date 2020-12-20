import scrapy

# Título = //h1/a/text()
# Citas = //span[@class="text" and @itemprop="text"]/text()
# Top ten tags = //div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()
# Next page button = //li[@class="next"]/a/@href

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/'
    ]
    custom_settings={
        'FEED_URI':'quotes.json',
        'FEED_FORMAT':'json',
        'CONCURRENT_REQUESTS': 24,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['camilogo1016@gmail.com'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'PepitoMi',
        'FEED_EXPORT_ENCODING':'utf-8'
    }

    def parse_only_quotes(self, response, **kwargs):
        if kwargs:
            quotes = kwargs['quotes']
            quotes.extend(response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall())
        
            #Acá selecciono la siguiente pagina
            next_page = response.xpath('//li[@class="next"]/a/@href').get()
            #Si esa página existe...
            if next_page:
                #repite la función "parse" usando el response de esa nueva pagina, ASÍ:
                yield response.follow(next_page, callback=self.parse_only_quotes, cb_kwargs={'quotes':quotes})
            else:
                yield {
                    'quotes' : quotes
                    }



    def parse(self, response):
        
        title = response.xpath('//h1/a/text()').get()
        
        quotes = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()
        
        top_tags = response.xpath('//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()
    
        top = getattr(self, 'top', None)
        
        if top:
            top = int(top)
            top_tags = top_tags[:top]
            

        yield {'title': title,
               'top_tags': top_tags}

        #Acá selecciono la siguiente pagina
        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        #Si esa página existe...
        if next_page:
            #repite la función "parse" usando el response de esa nueva pagina, ASÍ:
            yield response.follow(next_page, callback=self.parse_only_quotes, cb_kwargs={'quotes':quotes})


## en la terminal ponemos 
## scrapy crawl quotes -o quotes.json
    # el -o significa el output y después ponemos el archivo
    #   donde queremos que quede almacenado el output