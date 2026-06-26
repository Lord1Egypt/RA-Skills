---
name: uniqlo-price-watch
description: 跟踪 UNIQLO 网站（uniqlo.cn）上的产品价格，将用户关注的商品持久化存储在你的工作目录下 uniqlo/uniqlo-price-watch.csv 中，如果文件缺失则自动创建，并在回答用户前将当前官方产品页面价格与保存的基准价格进行比较。
version: 1.0.0
author: hcx
---

# UNIQLO 价格监控

当用户想要跟踪一个或多个 UNIQLO 产品、保存之前的价格，或询问关注的商品是否降价时，使用此技能。

# 用户追踪目标记录

当用户想要追踪一个项目时应当 把用户的 想要的商品记录到 uniqlo/uniqlo-price-watch.csv ，在用户表示 某某商品买到后，删除对应商品。

每次用户提供衣服时候，必须让用户确认 具体页面 https://www.uniqlo.cn/search.html?description=484663&searchType=1  且提供图片给用户，注意url不要记录商详页，而应该是搜索结果页

# uniqlo/uniqlo-price-watch.csv 格式

格式如下

商品名称,url,当前价格(rmb),上次价格(rmb),初始价格(rmb),更新时间
比如: 男装/男女同款 UT PEANUTS印花T恤/短袖T恤 485053,https://www.uniqlo.cn/search.html?description=484663&searchType=1,99,99,99,2026-3-22-10:52

# 如何获取商品价格
在用户添加监控商品时候，应当全部走 “获取商品价格的步骤-浏览器方案”。在后续监控任务中，在用户提供可用 fireCrawl API-KEY 的情况下(可以问用户要，或者读取环境变量 `FIRECRAWL_API_KEY`，兼容 `FIRECRAWL-API-KEY`)，应当先使用 “获取商品价格的步骤-爬虫方案”，使用 “获取商品价格的步骤-浏览器方案” 兜底。

获取商品价格的步骤-爬虫方案
[] 直接运行脚本，不要让大模型总结页面：
```
node .skills/uniqlo-price-watch/firecrawl-scrape.mjs \
  "https://www.uniqlo.cn/search.html?description=484663&searchType=1"
```
[] 脚本输出必须只保留这两个字段：
```
{
  "markdown": "...",
  "url": "https://www.uniqlo.cn/search.html?description=484663&searchType=1"
}
```
[] 从 `markdown` 中提取商品名称和价格；如果脚本失败，再使用浏览器方案兜底
 
获取商品价格的步骤-浏览器方案
[] 使用browser工具，访问优衣库的搜索页面: https://www.uniqlo.cn/search.html
[] 输入用户描述，选择优衣库搜索结果第一个商品
[] 点击进入商品页，拿到当前价格，并截图
[] 询问用户商品选择是否正确，如果正确更新到 uniqlo/uniqlo-price-watch.csv；如果错误回到第一步
