import json
import random
from urllib.parse import urljoin

import redis
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from settings import MOBILE_UA_FILE_PATH, PROXY_URL

r = redis.Redis()

with open(MOBILE_UA_FILE_PATH, 'r') as f:
    mobile_ua_list = [line.strip() for line in f.readlines()]


def get_mobile_ua():
    return random.choice(mobile_ua_list)


def get_proxy():
    # rv = list(r.hgetall('useful_proxy').keys())
    # return random.choice(rv) if rv else None

    try:
        ret_con = requests.get(urljoin(PROXY_URL, 'get_all')).content
        resp = json.loads(ret_con.decode('utf-8'))

        return random.choice(resp)
    except Exception as e:
        print(e)

        return None


def requests_retry_session(
        retries=3,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504),
        session=None
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self


if __name__ == '__main__':
    proxy_list = [get_proxy() for item in range(100)]
    print(proxy_list)
