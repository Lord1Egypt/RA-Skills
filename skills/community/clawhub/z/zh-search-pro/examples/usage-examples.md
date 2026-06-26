# 中文搜索增强工具 - 使用示例

## 示例 1：市场调研

```javascript
// 搜索 AI 行业报告
web_fetch({"url": "https://www.baidu.com/s?wd=2026+AI 行业报告+ filetype:pdf"})

// 搜索竞品分析
web_fetch({"url": "https://cn.bing.com/search?q=竞品分析+方法论&filters=ex1%3a%22last30%22"})

// 知乎专业讨论
web_fetch({"url": "https://www.zhihu.com/search?q=市场调研+方法&type=content"})
```

## 示例 2：内容创作素材

```javascript
// 搜索热点话题
web_fetch({"url": "https://www.baidu.com/s?wd=2026 热点话题+自媒体"})

// 微信爆款文章
web_fetch({"url": "https://weixin.sogou.com/weixin?type=2&query=爆款+写作技巧"})

// 今日头条热门
web_fetch({"url": "https://so.toutiao.com/search?keyword=创业+故事"})
```

## 示例 3：学术研究

```javascript
// 搜索学术论文
web_fetch({"url": "https://www.baidu.com/s?wd=site:cnki.net+机器学习"})

// 知乎专业回答
web_fetch({"url": "https://www.zhihu.com/search?q=深度学习+原理&type=answer"})

// 最新研究动态
web_fetch({"url": "https://cn.bing.com/search?q=AI+research+2026&filters=ex1%3a%22last7%22"})
```

## 示例 4：舆情监控

```javascript
// 品牌提及
web_fetch({"url": "https://www.baidu.com/s?wd=\"品牌名称\"+评价"})

// 微信讨论
web_fetch({"url": "https://weixin.sogou.com/weixin?type=2&query=产品名 + 评测"})

// 知乎讨论
web_fetch({"url": "https://www.zhihu.com/search?q=产品名 + 怎么样&type=content"})
```

## 示例 5：SEO 研究

```javascript
// 关键词排名
web_fetch({"url": "https://www.baidu.com/s?wd=目标关键词"})

// 竞争对手分析
web_fetch({"url": "https://www.baidu.com/s?wd=site:competitor.com"})

// 长尾关键词
web_fetch({"url": "https://cn.bing.com/search?q=如何+学习+python"})
```

## 组合使用技巧

```javascript
// 1. 先用百度搜索广泛信息
const baiduResults = web_fetch({"url": "https://www.baidu.com/s?wd=AI+创业"})

// 2. 再用知乎深入专业讨论
const zhihuResults = web_fetch({"url": "https://www.zhihu.com/search?q=AI+创业&type=content"})

// 3. 最后用微信查看实际案例
const wechatResults = web_fetch({"url": "https://weixin.sogou.com/weixin?type=2&query=AI+创业+案例"})

// 4. 综合分析
```

## 提示

- 搜索中文内容时，建议使用 UTF-8 编码的 URL
- 部分搜索引擎有反爬机制，可能需要重试
- 结合 `web_search` 工具（如果有 API 密钥）效果更佳
