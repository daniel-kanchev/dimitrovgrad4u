BOT_NAME = 'dimitrovgrad4u'
SPIDER_MODULES = ['dimitrovgrad4u.spiders']
NEWSPIDER_MODULE = 'dimitrovgrad4u.spiders'
ROBOTSTXT_OBEY = True
ITEM_PIPELINES = {
    'dimitrovgrad4u.pipelines.DatabasePipeline': 300,
}
LOG_LEVEL = 'WARNING'
