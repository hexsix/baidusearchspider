#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import pickle
import time

import requests
from fake_useragent import UserAgent

CACHE_FILENAME = 'proxy_cache'
PROXYSERVER_LIMIT_DELAY = time.time()


def get_new_headers():
    ua = UserAgent()
    # User-Agent 使用 fake_useragent, 并伪装成从 Google 跳转到 Baidu 进行搜索
    # 其他的都是从 Chrome 里扒下来的，可以自行更新
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
        'Connection': 'keep-alive',
        'Referer': 'https://www.google.com/',
        'User-Agent': ua.random,
    }
    return headers


class ProxyIpPool(object):
    def __init__(self, debug=0):
        self._set = set()
        self._lock = threading.Lock()
        self._debug = debug

    def pop(self):
        with self._lock:
            while not self._set:
                self._update()
            return self._set.pop()

    def push(self, elmnt):
        with self._lock:
            self._set.add(elmnt)

    def _test_proxy_delay(self, proxy, protocol='http', timeout=1):
        """ 测试与 www.baidu.com 的延迟
        :returns 延迟（秒），如果超时，返回 -1
        """
        session = requests.Session()
        session.headers = get_new_headers()
        test_url = 'https://www.baidu.com/s?ie=utf-8&tn=baidu&wd=NBA'
        with session:
            try:
                if self._debug:
                    print('\t\ttest proxy {}'.format(proxy))
                t = time.time()
                r = session.get(test_url, proxies={protocol: proxy}, timeout=timeout)
                if 'NBA' in r.text:
                    t = time.time() - t
                    if self._debug:
                        print('\t\t----test proxy {} succeeded within {} seconds'.format(proxy, t))
                    return t
                else:
                    raise Exception('html does not contain expected string')
            except Exception as e:
                if self._debug:
                    print('\t\t----test proxy {} failed: '.format(proxy) + str(e))
                return -1

    def _update(self):
        """ 从代理 IP 提供商处获取 IP，测试延迟并缓存在文件中
        你需要根据你自己的提供商 API 重写这个方法，
        如果你没有订阅，这里有一个免费的代理 IP：https://www.freeip.top/
        Thanks Aaron_JXL 请在这里查看这个代理的 API：https://github.com/jiangxianli/ProxyIpLib

        IP 非常珍贵，只要它们仍然可用，我们就不从提供商那里获取新的 IP，对此我将 IP 缓存在文件中
        """
        global PROXYSERVER_LIMIT_DELAY
        url = 'https://www.freeip.top/api/proxy_ips?country=%E4%B8%AD%E5%9B%BD'
        while time.time() - PROXYSERVER_LIMIT_DELAY < 2.0:
            continue  # 你必须要限制访问 API 的频率，否则你的 IP 会被 ban
        PROXYSERVER_LIMIT_DELAY = time.time()
        try:
            r = requests.get(url, timeout=2)
            if r.json()['msg'] == '成功':
                proxy_ips = [(item['protocol'], item['ip'] + ':' + item['port']) for item in r.json()['data']['data']]
                for proxy_ip in proxy_ips:
                    if proxy_ip[0] == 'https':
                        continue
                    delay = self._test_proxy_delay(proxy_ip[1], proxy_ip[0])
                    if delay != -1:  # if (delay := test_proxy_delay(proxy_ip[1], proxy_ip[0])) != -1:  # (py3.8)
                        self._set.add(proxy_ip[1])
            else:
                raise Exception('msg from freeip.top is not "成功"')
        except Exception as e:
            if self._debug:
                print('\tget proxies from freeip.top failed', e)

    def dump(self):
        with self._lock:
            with open(CACHE_FILENAME, 'wb') as f:
                pickle.dump(self._set, f)

    def load(self):
        with self._lock:
            with open(CACHE_FILENAME, 'rb') as f:
                self._set = pickle.load(f)
