---
name: Slug Generator
description: "Generate URL-friendly slugs from text. 将任意文本转换为SEO友好的URL别名，支持中英文混合、自动去除特殊字符。适合博客、电商、CMS系统。URL slug maker, permalink generator, URL safe string."
tags: slug, url, generator, seo, permalink, link, utility, tool
---

# Slug Generator 🔗

URL友好别名生成工具。

## Features | 功能

- **中英文支持**：中文转拼音Slug
- **特殊字符过滤**：自动移除不合规字符
- **多格式输出**：小写/大写/标题式

## Usage | 使用

```bash
# 基础转换
python3 scripts/slug.py "Hello World"

# 中文转拼音Slug
python3 scripts/slug.py "这是一个测试"

# 自定义分隔符
python3 scripts/slug.py "Hello World" --separator _

# 大写格式
python3 scripts/slug.py "Hello World" --uppercase
```

---

*免责声明：本工具仅供学习参考，不构成任何投资或商业建议。*
