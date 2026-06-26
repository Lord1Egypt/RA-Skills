# 国内搜索引擎深度搜索指南

> **版本**: v1.0.0 | **可用引擎**: 6/6

---

## 必应中国版 (Bing CN/INT)

### 特色功能

| 功能 | 说明 | URL |
|------|------|-----|
| **中文结果** | `ensearch=0` 返回中文结果 | `https://cn.bing.com/search?q={keyword}&ensearch=0` |
| **英文结果** | `ensearch=1` 返回英文结果 | `https://cn.bing.com/search?q={keyword}&ensearch=1` |
| **学术搜索** | 学术资源 | `https://cn.bing.com/academic/search?q={keyword}` |
| **中英切换** | 同一查询，两种语言结果 | 适合对比验证 |

### 高级语法

| 操作符 | 示例 | 说明 |
|--------|------|------|
| `site:` | `site:github.com python` | 站内搜索 |
| `""` | `"machine learning"` | 精确匹配短语 |
| `-` | `python -tutorial` | 排除关键词 |
| `filetype:` | `filetype:pdf report` | 指定文件类型 |

### 搜索示例

```javascript
// 中文搜索结果
web_fetch({"url": "https://cn.bing.com/search?q=人工智能技术&ensearch=0"})

// 英文搜索结果
web_fetch({"url": "https://cn.bing.com/search?q=artificial+intelligence&ensearch=1"})

// 学术搜索
web_fetch({"url": "https://cn.bing.com/academic/search?q=机器学习算法"})

// 站内搜索
web_fetch({"url": "https://cn.bing.com/search?q=site:zhihu.com+Python"})
```

---

## 360搜索

### 特色功能

| 功能 | 说明 | URL |
|------|------|-----|
| **安全搜索** | 内置安全防护，过滤广告 | 默认开启 |
| **基础搜索** | 网页搜索 | `https://www.so.com/s?q={keyword}` |
| **新闻搜索** | 新闻聚合 | `https://news.so.com/news?q={keyword}` |
| **图片搜索** | 图片索引 | `https://image.so.com/i?q={keyword}` |

### 搜索示例

```javascript
// 基础搜索
web_fetch({"url": "https://www.so.com/s?q=网络安全"})

// 站内搜索
web_fetch({"url": "https://www.so.com/s?q=site:zhihu.com+python教程"})

// 新闻搜索
web_fetch({"url": "https://news.so.com/news?q=AI人工智能"})
```

---

## 头条搜索 (Toutiao)

### 特色功能

| 功能 | 说明 | URL |
|------|------|-----|
| **资讯丰富** | 自媒体、新闻资讯聚合 | `https://www.toutiao.com/search/?keyword={keyword}` |
| **算法推荐** | 内容质量高，推荐精准 | 适合深度阅读 |
| **热点追踪** | 实时热点内容 | 舆情分析 |

### 搜索示例

```javascript
// 资讯搜索
web_fetch({"url": "https://www.toutiao.com/search/?keyword=AI大模型最新进展"})

// 科技新闻
web_fetch({"url": "https://www.toutiao.com/search/?keyword=人工智能+技术突破"})
```

---

## B站搜索 (Bilibili)

### 特色功能

| 功能 | 说明 | URL |
|------|------|-----|
| **视频教程** | 编程、技术教程视频 | `https://search.bilibili.com/all?keyword={keyword}` |
| **视频类型** | 支持按类型筛选 | `all`（综合）、`video`（视频）、`bangumi`（番剧）、`article`（专栏） |
| **排序** | 默认排序方式 | `order=总排行`、`order=最新发布`、`order=最多点击` |

### 搜索示例

```javascript
// 综合搜索
web_fetch({"url": "https://search.bilibili.com/all?keyword=Python教程"})

// 视频教程
web_fetch({"url": "https://search.bilibili.com/video?keyword=爬虫+实战"})

// 技术专栏
web_fetch({"url": "https://search.bilibili.com/article?keyword=AI大模型"})
```

---

## 必应学术 (Bing Academic)

### 特色功能

| 功能 | 说明 | URL |
|------|------|-----|
| **国际+中文学术** | 论文、期刊、会议论文 | `https://cn.bing.com/academic/search?q={keyword}` |
| **多维检索** | 支持作者、期刊、关键词 | 学术索引全面 |

### 搜索示例

```javascript
// 学术论文搜索
web_fetch({"url": "https://cn.bing.com/academic/search?q=深度学习+图像识别"})

// 特定主题论文
web_fetch({"url": "https://cn.bing.com/academic/search?q=transformer+attention"})
```

---

## 国内搜索策略

### 按目标选择引擎

| 搜索目标 | 首选引擎 | 备选 | 原因 |
|---------|---------|------|------|
| **综合中文内容** | 必应中国 | 360 | 中英文兼顾，稳定可用 |
| **英文技术文档** | 必应国际 | 无 | 一键切换英文结果 |
| **学术论文** | 必应学术 | 无 | 国际+中文学术索引 |
| **新闻热点** | 头条 | 无 | 实时资讯聚合 |
| **视频教程** | B站 | 无 | 技术视频最全 |

### 已移除引擎说明

以下引擎经实测确认被反爬拦截或403限制，无法通过web_fetch或agent-browser正常访问，已从搜索引擎中移除。如需使用，请通过浏览器手动访问：

| 原引擎 | 拦截类型 | 手动访问建议 |
|--------|---------|-------------|
| 百度 | CAPTCHA滑块 | PC浏览器访问 www.baidu.com |
| 百度学术 | CAPTCHA图形 | PC浏览器访问 xueshu.baidu.com |
| 搜狗 | 反爬页 | PC浏览器访问 www.sogou.com |
| 搜狗微信 | 反爬页 | PC浏览器访问 wx.sogou.com |
| 微博 | 登录墙 | 登录后访问 s.weibo.com |
| 知乎 | 403禁止访问 | 登录后访问 www.zhihu.com |
| 神马 | TMD反爬验证 | 需执行JS通过验证，web_fetch不支持 |
| 夸克 | TMD反爬验证 | 同上 |

---

## 参考资料

- [必应搜索技巧](https://cn.bing.com/tips)
- [360搜索帮助](https://www.so.com/help.html)
