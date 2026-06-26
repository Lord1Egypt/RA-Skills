# Smart Crawler - 智能爬虫工具

企业级爬虫解决方案，支持动态渲染、反爬虫绕过、分布式爬取。

## 功能特性

- 🕷️ **多引擎支持**：Scrapy(批量)、Playwright(动态)、requests(轻量)
- 🛡️ **反爬虫对抗**：IP 代理池、请求频率控制、User-Agent 轮换
- 📊 **智能解析**：XPath、CSS Selector、正则、JSONPath
- 💾 **数据存储**：JSON、CSV、Excel、MongoDB、MySQL
- 📈 **监控面板**：实时爬取统计、失败重试、日志记录
- 🔄 **任务调度**：定时任务、增量更新、断点续爬

## 安装

```bash
pip install -r requirements.txt

# Playwright 浏览器
playwright install chromium
```

## 依赖要求

- Python 3.8+
- requests >= 2.28
- scrapy >= 2.10
- playwright >= 1.35
- beautifulsoup4 >= 4.12
- lxml >= 4.9
- fake-useragent >= 1.2

## 快速开始

### 简单爬取

```python
from scripts.crawler import Crawler

crawler = Crawler()
html = crawler.fetch('https://example.com')
data = crawler.extract(html, {
    'title': '//h1/text()',
    'price': '.price::text'
})
print(data)  # {'title': '...', 'price': '...'}
```

### 批量爬取

```python
from scripts.batch_crawler import BatchCrawler

urls = ['https://site.com/page/{}'.format(i) for i in range(1, 11)]
crawler = BatchCrawler(concurrent=5, delay=(1, 3))
results = crawler.crawl(urls)
```

### 动态页面

```python
from scripts.dynamic_crawler import DynamicCrawler

crawler = DynamicCrawler()
html = crawler.fetch('https://spa-app.com', wait_for='.content-loaded')
data = crawler.extract(html, {'items': '.product-item'})
```

## API 文档

### Crawler

```python
Crawler(proxy_pool=None, delay_range=(0, 0), user_agent='rotate')
```

| 参数 | 类型 | 说明 |
|------|------|------|
| proxy_pool | ProxyPool | 代理池实例 |
| delay_range | tuple | 请求间隔范围(秒) |
| user_agent | str | User-Agent策略 |

### 提取规则

```python
# XPath
data = crawler.extract(html, {'title': '//h1/text()'})

# CSS Selector
data = crawler.extract(html, {'price': '.price::text'})

# 属性提取
data = crawler.extract(html, {'link': 'a::attr(href)'})

# JSONPath (for JSON response)
data = crawler.json_extract(json_data, '$.items[*].name')
```

## 反爬虫策略

### 代理池

```python
from scripts.proxy_pool import ProxyPool

pool = ProxyPool([
    'http://proxy1:8080',
    'http://user:pass@proxy2:8080'
])
crawler = Crawler(proxy_pool=pool)
```

### 请求频率控制

```python
crawler = Crawler(
    delay_range=(1, 3),
    max_retries=3,
    timeout=30
)
```

## 示例

见 `examples/basic_usage.py`

## 测试

```bash
python -m pytest tests/ -v
```

## 许可证

MIT License
