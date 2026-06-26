# 平台热榜数据抓取指南

各大平台热榜数据的抓取方法。

## 微博热搜

```bash
# 实时热搜榜（无需登录）
curl "https://weibo.com/ajax/side/hotSearch" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
```

返回字段：`realtime[].word`（词条）、`realtime[].num`（热度值）、`realtime[].label_name`（标签：爆/热/新）

## 抖音热榜

```bash
# 抖音热榜（需要 Cookie）
curl "https://www.douyin.com/aweme/v1/web/hot/search/list/?device_platform=webapp&aid=6383" \
  -H "Cookie: YOUR_COOKIE" \
  -H "Referer: https://www.douyin.com/"
```

返回字段：`data.word_list[].word`（词条）、`data.word_list[].hot_value`（热度）

## 知乎热榜

```bash
# 知乎热榜（无需登录）
curl "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50" \
  -H "User-Agent: Mozilla/5.0"
```

返回字段：`data[].target.title`（问题标题）、`data[].detail_text`（热度描述）

## 百度热搜

```bash
# 百度实时热点
curl "https://top.baidu.com/api/board?platform=wise&tab=realtime" \
  -H "User-Agent: Mozilla/5.0"
```

返回字段：`data.cards[0].content[].word`（词条）、`data.cards[0].content[].hotScore`（热度分）

## 小红书热门

小红书无公开 API，建议通过搜索页面抓取：
```bash
# 搜索热门笔记（需要 Cookie）
curl "https://www.xiaohongshu.com/api/sns/web/v1/search/notes?keyword=KEYWORD&page=1&page_size=20&sort=general" \
  -H "Cookie: YOUR_COOKIE"
```

## B站热门

```bash
# B站热门视频（无需登录）
curl "https://api.bilibili.com/x/web-interface/popular?ps=20&pn=1" \
  -H "User-Agent: Mozilla/5.0"
```

返回字段：`data.list[].title`（标题）、`data.list[].stat.view`（播放量）

## 注意事项

- 微博、知乎、百度热搜无需 Cookie，可直接抓取
- 抖音、小红书需要有效 Cookie，建议从浏览器开发者工具获取
- 建议抓取间隔 ≥ 5 分钟，避免被限流
- 部分平台会定期更新反爬策略，如遇 403/429 需更新 Cookie 或 UA
