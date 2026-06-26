---
name: wechat-articles
description: >
  搜索和读取微信公众号文章的完整工具，支持关键词搜索与全文提取。
  **只要用户提到以下任何场景，必须使用此 skill：**
  (1) 搜索公众号文章、按关键词查找微信内容
  (2) 读取、摘要、分析、翻译 mp.weixin.qq.com 链接的内容
  (3) 用户说"帮我找公众号文章"、"读这篇微信文章"、"搜索公众号"、"抓取公众号"
  (4) 用户粘贴了微信文章 URL 并要求提取或处理内容
  (5) 需要从微信生态获取资讯、报告、行业信息
  即使用户没有明确说"微信"，只要涉及公众号内容获取或提取，也应触发此 skill。
  Triggers: 搜索公众号, 微信文章, 读这篇公众号, 抓取公众号, wechat article, mp.weixin.qq.com, 公众号内容, 微信链接
version: 1.0.0
homepage: https://github.com/johan-oilman/wechat-articles
author: 油太人 / @johan-oilman
license: MIT
metadata:
  clawdbot:
    emoji: "📄"
    requires:
      packages:
        - beautifulsoup4
        - requests
        - playwright
        - miku-ai
      binaries:
        - chromium
      install:
        - pip install beautifulsoup4 requests playwright miku-ai
        - playwright install chromium --with-deps
---

# 微信公众号文章搜索与读取 (v1.0)

搜索和读取微信公众号文章的完整工具，支持 **simple**（快速）和 **playwright**（稳定）双模式 + **auto** 自动切换。

## 快速开始

### 搜索文章
```bash
python3 scripts/search.py "关键词" [数量]
```
示例：
```bash
python3 scripts/search.py "绿电直连政策" 10
```

### 读取文章
```bash
python3 scripts/read.py "微信文章URL" [--mode MODE] [--screenshot PATH]
```
模式选择：
- `--mode=simple` - 快速模式（requests + BeautifulSoup）
- `--mode=playwright` - 稳定模式（真实浏览器）
- `--mode=auto` - 自动切换（默认，推荐）

## Python API 使用（推荐）

```python
import sys
sys.path.append('scripts')

from wechat_articles import search_articles, read_article

# 搜索文章
articles = search_articles("绿电直连政策", top_num=5)

# 读取文章（建议加错误处理）
try:
    content = read_article(articles[0]['url'], mode='auto')
    print(f"标题: {content['title']}")
    print(f"公众号: {content['author']}")
    print(f"发布时间: {content['publish_time']}")  # 若有
    print(f"读取模式: {content['mode']}")
    for p in content['paragraphs'][:10]:
        print(p)
except Exception as e:
    print(f"读取失败: {e}")
    # auto 模式失败时会抛出异常，建议捕获后降级处理或提示用户
```

### 返回数据结构说明

`read_article()` 返回一个字典，包含以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `title` | str | 文章标题 |
| `author` | str | 公众号名称 |
| `publish_time` | str | 发布时间（部分文章可能为空） |
| `paragraphs` | list[str] | 正文段落列表 |
| `mode` | str | 实际使用的读取模式（`simple` 或 `playwright`） |

`search_articles()` 返回列表，每项包含：

| 字段 | 类型 | 说明 |
|------|------|------|
| `title` | str | 文章标题 |
| `url` | str | 文章链接（有时效性，建议尽快读取） |
| `author` | str | 公众号名称 |
| `digest` | str | 文章摘要 |

## 模式对比

| 模式 | 速度 | 资源 | 稳定性 | 适用场景 |
|------------|------------|------|--------|----------------------|
| simple | 快 (0.5-1s) | 轻量 | 一般 | 简单页面，频繁调用 |
| playwright | 慢 (3-5s) | 较重 | 很高 | 复杂页面，稳定优先 |
| auto | 自适应 | 自适应 | 最佳 | 默认推荐 |

## 安装依赖

### Simple 模式（默认，轻量快速）
```bash
pip install beautifulsoup4 requests miku-ai
```
这些包通常已随 agent-reach 安装。

### Playwright 模式（可选，推荐稳定读取）
```bash
pip install playwright
playwright install chromium --with-deps
```
`--with-deps` 会自动安装 Linux 系统依赖（如 libnss3、libgbm 等），首次运行需几分钟。

## 注意事项

- 搜索结果 URL 有时效性，建议尽快读取
- 避免高频请求防止触发反爬
- auto 模式优先尝试 simple，失败后自动切换 playwright；若两者均失败则抛出异常
- Playwright 首次运行需安装 Chromium（约几分钟）

欢迎反馈 & PR！GitHub: https://github.com/johan-oilman/wechat-articles
