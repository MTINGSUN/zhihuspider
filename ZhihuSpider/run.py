import scrapy  
from scrapy.crawler import CrawlerProcess  
from scrapy.utils.project import get_project_settings
from ZhihuSpider.spiders.ZH import ZhSpider
# from ZhihuSpider.spiders.ProxiesSpider import ProxiesSpider

process = CrawlerProcess(get_project_settings())  

# process.crawl(ProxiesSpider)
process.crawl(ZhSpider)  
process.start() # the script will block here until the crawling is finished  