import csv
import string
from multiprocessing.pool import ThreadPool

from requests.exceptions import ConnectTimeout, ConnectionError, ProxyError

from settings import *
from utils.utils import *


class CrawlError(Exception):
    ...


def crawl(writer, page=1):
    print(f'Starting fetch Page {page}')
    callback_str = ''.join(random.sample(string.ascii_letters, 2))
    session = requests_retry_session()
    for i in range(DEFAULT_RETRIES):
        if i == DEFAULT_RETRIES - 1:
            proxies = None
        else:
            proxies = {'https': get_proxy()}
        try:
            r = session.get(SEARCH_PAGE.format(page=page, keyword=KEYWORD, callback_str=callback_str),
                            proxies=proxies,
                            timeout=TIMEOUT,
                            headers={'User-Agent': get_mobile_ua()})
        except ProxyError:
            print(f'Proxy {proxies} is dead!')
        except (ConnectTimeout, ConnectionError):
            ...
        else:
            break
    print(f'Fetched Page {page}')
    try:
        rv = AttrDict(json.loads(ESCAPE_REGEX.sub('', r.text[20:-2])))
    except json.decoder.JSONDecodeError as e:
        raise CrawlError(e)

    if rv.errmsg:
        raise CrawlError(rv.errmsg)
    items = rv.data['searchm']['Paragraph']

    for item in items:
        item = AttrDict(item)

        row = (
            item.Content['warename'],
            ''.join((IMG_URL_HOST + item.Content['imageurl'])),
            item.Content['author'],
            item.dredisprice,
            item.commentcount,
            item.good,
            item.shop_name,

        )

        writer.writerow(row)


def run_crawl(max_page=MAX_PAGE, thread_max=5):
    with open(RESULT_SAVE_PATH, 'wt', newline='') as fp:
        writer = csv.writer(fp)
        writer.writerow(('标题', '封面图片地址', '作者', '价格', '评论数', '好评率', '商店名'))
        pool = ThreadPool(thread_max)
        pool.starmap(crawl, [(writer, page) for page in range(1, max_page + 1)])
    pool.close()
    pool.join()
