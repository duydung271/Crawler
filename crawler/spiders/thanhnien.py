import scrapy



class PaperSpider(scrapy.Spider):
    name = "thanhnien"
    labels =[ 'kinh-doanh','giai-tri','giao-duc','the-thao', 'suc-khoe',]
    stt_page =1
    start_urls = [
        'https://thanhnien.vn/tai-chinh-kinh-doanh',
        'https://thanhnien.vn/giai-tri',
        'https://thanhnien.vn/giao-duc',
        'https://thanhnien.vn/the-thao',
        'https://thanhnien.vn/suc-khoe',
    ]
    def parse(self, response):
        for i,label in enumerate(self.labels):
            if label in response.url:
                self.label=label
                break
        for paper_href in response.css('div.relative article.story a::attr(href)'):
            if paper_href is not None:
                yield response.follow(paper_href, self.parse_post)

        next_page = response.css('ul.pagination li a::attr(href)').getall()[-1]
        if  response.css('ul.pagination li a::attr(title)').getall()[-1] == 'Trang sau':
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)

    def parse_post(self, response):
        content = response.css('div.details')
        if content.css('h2.details__headline::text').get() is not None:
            copurs =""
            for paragraph in response.css('div.cms-body.detail p::text').getall():
                copurs+=paragraph+" "
            yield{
                'label': self.label,
                'link': response.url,
                'title':content.css('h2.details__headline::text').get(),
                'description':content.css('div.sapo.cms-desc p::text').get(),
                'content':copurs
            }


                     

        
