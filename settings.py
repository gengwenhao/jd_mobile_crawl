"""
    爬虫的配置
"""
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 代理地址
PROXY_URL = 'http://192.168.33.13:5010/'

# 查找关键字
KEYWORD = '考研数学'

# 最大页数
MAX_PAGE = 100

# 延时
TIMEOUT = 2

DEFAULT_RETRIES = 5

SEARCH_PAGE = 'https://so.m.jd.com/ware/search._m2wq_list?keyword={keyword}&datatype=1&callback=jdSearchResultBkC{callback_str}&page={page}&pagesize=10&ext_attr=no&brand_col=no&price_col=no&color_col=no&size_col=no&ext_attr_sort=no&merge_sku=yes&multi_suppliers=yes&area_ids=5,224,3156&qp_disable=no&fdesc=%E6%B2%B3%E5%8C%97&t1=1548755096975'  # noqa

ESCAPE_REGEX = re.compile(r'\\(?![/u"])')

# 商品封面图片服务器地址
IMG_URL_HOST = 'https://img10.360buyimg.com/mobilecms/s455x455_'

# 结果保存路径
RESULT_SAVE_PATH = os.path.join(BASE_DIR, 'result.csv')

# 手机UA文件
MOBILE_UA_FILE_PATH = os.path.join(BASE_DIR, 'utils', 'mobile_ua.txt')
