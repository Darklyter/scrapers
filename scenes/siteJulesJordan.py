import re

import scrapy
from tpdb.BaseSceneScraper import BaseSceneScraper


class JulesJordanSpider(BaseSceneScraper):
    name = 'JulesJordan'
    network = 'julesjordan'
    parent = 'julesjordan'

    start_urls = [
        'https://www.julesjordan.com',
        'https://www.manuelferrara.com',
        'https://www.theassfactory.com',
        'https://www.spermswallowers.com',
        'https://www.girlgirl.com'
    ]

    selector_map = {
        'title': '//span[@class="title_bar_hilite"]/text()',
        'description': '//span[@class="update_description"]/text()',
        'date': '//div[@class="cell update_date"]/text()',
        'performers': '//div[@class="backgroundcolor_info"]/span[@class="update_models"]/a/text() | //div[@class="gallery_info"]//span[@class="update_models"]/div[@class="container"]/a/text()',
        'tags': '//span[@class="update_tags"]/a/text()',
        'external_id': 'trial\\/scenes\\/(.+)\\.html',
        'trailer': '',
        'pagination': '/trial/categories/movies_%s_d.html'
    }

    max_pages = 47

    def get_scenes(self, response):
        scenes = response.xpath(
            "//div[@class='category_listing_wrapper_updates']//a[1]/@href").getall()
        for scene in scenes:
            if re.search(self.get_selector_map('external_id'), scene):
                yield scrapy.Request(url=scene, callback=self.parse_scene)

    def get_image(self, response):
        result = re.search('useimage = "(.+?)";', response.text)
        if result:
            return self.format_link(response, result.group(1))
