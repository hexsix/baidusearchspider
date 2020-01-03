#!/usr/bin/env python
# -*- coding: utf-8 -*-
from concurrent.futures.thread import ThreadPoolExecutor

import requests
from lxml import etree
from newspaper import Article, Config
from proxy_ip_pool import get_new_headers, ProxyIpPool

DEBUG = 0
BAIDU_HOST_URL = "http://www.baidu.com"
BAIDU_SEARCH_URL = "http://www.baidu.com/s?ie=utf-8&tn=baidu&wd="
PROXY_POOL = ProxyIpPool()


def multi_thread_search(querys, num_results=10):
    if DEBUG:
        print('multi search start: debug print may be a mess cuz multi threads')
    res = [None] * len(querys)
    with ThreadPoolExecutor(max_workers=10) as executor:
        for i, query in enumerate(querys):
            res[i] = executor.submit(single_thread_search, query, num_results)
    return [item.result() for item in res if item.done()]


def single_thread_search(query, num_results=10):
    if DEBUG:
        print('single search starts: query is', query)
    s = search(query, num_results)
    ret = {'query': query, 'urls': s}
    if DEBUG:
        print('----single search ends:', query)
    return ret


def search(query, num_results=10, retry=2):
    urls = None
    for i in range(retry):
        session = requests.Session()
        session.headers = get_new_headers()
        # headers can't be None
        proxy_ip = PROXY_POOL.pop()
        session.proxies = {'http': proxy_ip}
        with session:
            try:
                urls = baidu_search(session, query, num_results)
            except Exception:
                continue
            if urls:
                PROXY_POOL.push(proxy_ip)
                break
    if urls:
        return urls
    else:
        return None


def baidu_search(session, query, num_results):
    total_urls = []
    next_url = BAIDU_SEARCH_URL + query
    while len(total_urls) < num_results and next_url:
        html = session.get(next_url, timeout=1)
        html.encoding = 'utf-8'
        tree = etree.HTML(html.text)
        urls = []
        h3_selectors = tree.xpath('//h3/a')
        for i, sel in enumerate(h3_selectors):
            # title = sel.xpath('text()')[0]
            href = sel.xpath('@href')[0]
            # href = session.get(href).url
            urls.append(href)
        if urls:
            total_urls += urls
        try:
            next_url = BAIDU_HOST_URL + tree.xpath('//a[@class="n"]/@href')[0]
        except Exception:
            next_url = None
    return total_urls


def get_article(url):
    config = Config()
    config.request_timeout = 1.3
    article = Article(url, language='zh', config=config)
    try:
        article.download()
        article.parse()
        # article.nlp()
    except Exception:
        return
    return article.text


def single_thread_get_article(url):
    a = get_article(url)
    news = {"url": url, "content": a}
    return news


def get_articles(urls):
    res = [None] * len(urls)
    with ThreadPoolExecutor(max_workers=100) as executor:
        for i, url in enumerate(urls):
            res[i] = executor.submit(single_thread_get_article, url)
    return [item.result() for item in res if item.done()]


if __name__ == '__main__':
    DEBUG = 1
    PROXY_POOL = ProxyIpPool(DEBUG)
    PROXY_POOL.load()
    _querys = ['1096', '114514', '9876543210.33', '1000-7']
    _ret = multi_thread_search(_querys)
    # _ret = single_thread_search('zdasdq', num_results=10)
    PROXY_POOL.dump()
    # for _ in _ret:
    #     print(_)
    # print(_ret)
    aaa = get_articles(_ret[1]['urls'])
    print(aaa)
    pass
