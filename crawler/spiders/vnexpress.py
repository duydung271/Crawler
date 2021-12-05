import scrapy


class PaperSpider(scrapy.Spider):
    name = "vnexpress"
    start_urls = [
        'https://vnexpress.net/kinh-doanh',
    ]
    def parse(self, response):
        labels= response.url.split('/')[-1].split('-')
        self.label = labels[0]+'-'+labels[1]

        for paper_href in response.css('p.description a::attr(href)'):
            if paper_href is not None:
                yield response.follow(paper_href, self.parse_post)

        # next_page = response.css('div.button-page a.next-page::attr(href)').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
        next_page = response.css('div.button-page a.next-page::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_post(self, response):
        content = response.css('div.sidebar-1')
        if content.css('h1.title-detail::text').get() is not None:
            copurs =""
            for paragraph in response.css('article.fck_detail p::text').getall():
                copurs+=paragraph+" "
            yield{
                'label': self.label,
                'link': response.url,
                'title':content.css('h1.title-detail::text').get(),
                'description':content.css('p.description::text').get(),
                'content':copurs
            }


                     

        
