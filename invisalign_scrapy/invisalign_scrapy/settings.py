# -*- coding: utf-8 -*-

# Scrapy settings for invisalign_scrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'invisalign_scrapy'

SPIDER_MODULES = ['invisalign_scrapy.spiders']
NEWSPIDER_MODULE = 'invisalign_scrapy.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'invisalign_scrapy (+http://www.yourdomain.com)'
AUTO_THROTTLE_ENABLED = True