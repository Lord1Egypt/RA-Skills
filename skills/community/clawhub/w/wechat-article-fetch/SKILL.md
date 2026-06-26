---
name: wechat-article-fetch
description: 提取微信公众号文章内容。支持获取文章标题、作者、发布时间、正文内容等。当用户需要读取、总结、分析微信公众号文章时使用。
---

# WeChat Article Fetch 技能

提取微信公众号文章（mp.weixin.qq.com）的完整内容。

## 功能特点

- ✅ 提取文章标题、作者、发布时间
- ✅ 获取完整正文内容（纯文本）
- ✅ 自动处理微信公众号的特殊 HTML 结构
- ✅ 支持长文章（无长度限制）
- ✅ 可提取文章链接和二维码信息

## 使用方法

### 提取文章内容

```python
from skills.wechat_article_fetch import fetch_article

# 获取文章完整信息
article = fetch_article("https://mp.weixin.qq.com/s/fGlf05NkMHQlbW_VMjacuA")

print(f"标题：{article['title']}")
print(f"作者：{article['author']}")
print(f"发布时间：{article['publish_time']}")
print(f"内容长度：{len(article['content'])} 字符")
print(f"摘要：{article['content'][:200]}...")
```

### 只获取文本内容

```python
from skills.wechat_article_fetch import get_article_text

text = get_article_text("https://mp.weixin.qq.com/s/xxx")
print(text)
```

### 获取文章元数据

```python
from skills.wechat_article_fetch import get_article_metadata

meta = get_article_metadata("https://mp.weixin.qq.com/s/xxx")
print(meta)
# 返回：{'title': '...', 'author': '...', 'publish_time': '...', 'account': '...'}
```

## 返回数据格式

```python
{
    'title': str,          # 文章标题
    'author': str,         # 作者
    'publish_time': str,   # 发布时间
    'account': str,        # 公众号名称
    'content': str,        # 正文内容（纯文本）
    'url': str,            # 文章链接
    'raw_html': str,       # 原始 HTML（可选）
    'extracted_at': str    # 提取时间
}
```

## 使用场景

- 📰 总结微信公众号文章
- 🔍 分析文章内容
- 📊 提取文章数据
- 🤖 训练 AI 模型
- 📝 保存文章归档

## ⚠️ 依赖安装（必须先安装）

使用前请安装依赖：
```bash
pip install beautifulsoup4 requests
```

或在虚拟环境中：
```bash
python -m pip install beautifulsoup4 requests
```

## 注意事项

1. 需要网络连接才能下载文章
2. 部分付费文章可能无法访问
3. 过于古老的文章可能已被删除
4. **必须先安装依赖库**（beautifulsoup4 + requests）

## 安全说明

本技能仅用于提取公开的微信公众号文章内容，不包含任何自动执行系统命令的代码。

## 示例

```python
from skills.wechat_article_fetch import fetch_article, summarize_article

# 获取并总结文章
article = fetch_article("https://mp.weixin.qq.com/s/xxx")
summary = summarize_article(article['content'], max_length=500)

print(f"文章：{article['title']}")
print(f"摘要：{summary}")
```

## 技术实现

- 使用 `curl` 下载网页（模拟浏览器 User-Agent）
- 使用 `BeautifulSoup` 解析 HTML
- 定位 `#js_content` 或 `.rich_media_content` 区域
- 提取纯文本并清理格式

---

*创建时间：2026-03-24*  
*版本：1.0.0*
