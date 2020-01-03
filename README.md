# Simple Baidu Search Spider

## Description

随便写的，本项目帮助那些不熟悉爬虫，但是想要小批量爬取一些百度搜索结果的吃瓜群众。

写 BUG 专家，随便用用还行，如果要 100% 的保障，还是用 Scrapy 比较好。

## Installation

本食品必要的第三方包：
* requests
* fake_useragent
* lxml

本食品可选的第三方包
* newspaper （用于解析百度搜索结果链接内的文章）

## Usages

```python console
>>> from baidusearchspider import single_thread_search, multi_thread_search, get_articles

>>> nba = single_thread_search('NBA')
>>> nba
{'query': 'NBA',
 'urls': ['http://www.baidu.com/link?url=a3WyWJnovGBCEqyqX3FFdMjZUjIBarCnKp_YeQCCQuW',
  'http://trust.baidu.com/vstar/official/intro?type=gw',
  'http://www.baidu.com/link?url=Y77SWA_hR2XmlaE9LQmvaPgRebJNBkpATBRW75KtPGed8jarb6p6X3wJ4XlIzWEL',
  'http://www.baidu.com/link?url=gM_Ayth_rQKeUPOm5mLVUPezHomW9CcCFZYFTxRo7-e',
  'http://www.baidu.com/link?url=3Ya-y5P4BRAmynHEpOsAmwkBIjFkeUcD1dT39Qyi0aoy9q_6tPUFsuwAIs4_vyP8UmmckAWxy2S3PVtqh7bjMKTSrLo_I8dqSH3z14Lelci',
  'http://www.baidu.com/link?url=IRodiMufH8uH733v4hGm_PPIaIeYsGSsATW5WQxBe6mVUEho0AdkKWr2PUM05oWPTblk6TcvQxz0JlPNTN3JTa',
  'http://www.baidu.com/link?url=merLLwlnKmYd0zDaMWL1S3ItxeSwqfLVDI1vs5Vt_llYkWjvD2YtcM0ZMEm2662Z',
  'http://www.baidu.com/link?url=kQS_zRdTdqRYjJipLPu9OpaTn9Q8mK67P_ezJSvgoWq',
  'http://www.baidu.com/link?url=7DfSz_yykxaqTgy5rFJxS0XWsyvycc3M05A9msaqqu30htPsMX7WNqukfibVxp_s8GrotRQjbvntLn7HXtxrlV8CeluaMsC7mlg5TZZrgYW',
  'http://www.baidu.com/link?url=kBPbaBwC_zFmtR1fvr9Wlg2afAzxW_LjrZubwVm6C8a']}
>>> # 如果答案是 'urls': None，多试几次

>>> sss = multi_thread_search(['1096', '114514', '9876543210.33', '1000-7'])
>>> sss
[{'query': '1096','urls': ['http://www.baidu......]},
 {'query': '114514','urls': ['http://www.baidu......]},
 {'query': '9876543210.33','urls': ['http://www.baidu......]},
 {'query': '1000-7','urls': ['http://www.baidu......]}]

>>> aaa = get_articles(sss[0]['urls'])
>>> aaa
[{'url': 'http://www.baidu.com/link?url=iLGfNvygvi-5xdLZBIj_-2h84FpUq8tjK52C5qvWC0ToOubo6ZA234F4e-A5Td9A',
  'content': '基本资料 姓名 朝比奈 （ あさひな ） みくる\n\n（Asahina Mikuru） 别号 1096 身高 152cm 三围 这是禁止事项 年龄 这是禁止事项......'},
 {'url': 'http://www.baidu.com/link?url=IKAy0FTyiENAtR_r3ChGzMZMBbSTY4-Zo9fLm4cLYX778Ze4OfmUYIhink6jOSTAs_mhnt0sEZ3QZ4WTZRPI1a',
  'content': '哈哈。放水啦。我带头…………有啥放的水在这里发就好了。PS:文明放水哦。忌黑。忌黄。忌暴力！'},
 {'url': 'http://www.baidu.com/link?url=Pg0W24fHZwH2Da6ywiBcVLy2ItqODayTU49o-WNDlu9_aj-elXej5zrb52oxZPAGWSwMPaOvXil_yacAMFExLq',
  'content': '展开全部\n\n1096即是指的朝比奈实玖瑠（10，9，6与实玖瑠谐音），出自作品《凉宫春日系列》轻小说以及其改编系列动画中。1096最萌就是......'},
 {'url': 'http://www.baidu.com/link?url=h_RaAbD93tTUWEMCbBBnsdSUIkD-KcZV4E-MK1azSUqtExsuLMC80pOADXJWRVMhmXGBTKbIyD41miEpf3OjZO93Lse_ZCVYOV0ccItPQNy',
  'content': '1096年 编辑 锁定 讨论\n\n中文名 1096年 外文名 1096 year\n\n目录 1 大事记 ▪ 欧洲： ▪ 牛津大学 ▪ 中国 2 出生 3 逝世\n\n......'},
 {'url': 'http://www.baidu.com/link?url=peUQI10yCYSuL9SNLGDWSovyiHP5jG191M8V3Oqlv74TK6O4VnVF2_AbTAAuwA0fggJr6CbXjIm-zW0X9dX8X_',
  'content': '\ue768 我来答\n\n可选中1个或多个下面的关键词，搜索相关资料。也可直接点“搜索资料”搜索整个问题。'},
 {'url': '/sf/vsearch?pd=video&tn=vsearch&lid=81a1ad8500133405&ie=utf-8&rsv_pq=81a1ad8500133405&wd=1096&rsv_spt=5&rsv_t=c6c13NdgtEPBs25xHNjjwUm19IWbCKt8YSOQiZGswgR8J27qRM1baYSpQnw&rsv_bp=1&f=8',
  'content': None},
 ......
>>> # /sf/... 这种是百度指向自家产品的链接，不爬也可以
```

## Thanks

感谢 Aaron_JXL 提供的免费的代理 IP：https://www.freeip.top/

请在这里查看这个代理的 API：https://github.com/jiangxianli/ProxyIpLib
