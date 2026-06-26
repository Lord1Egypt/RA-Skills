# 示例文章目录

此目录用于存放待发布的文章。

## 使用方法

1. 在此目录创建 Markdown 文件
2. 文件头部包含元信息（title, categories, tags）
3. 使用发布脚本发布

## 示例

```bash
# 创建文章
cat > articles/my-post.md << 'MARKDOWN'
---
title: 我的文章
categories: 分类 1, 分类 2
tags: 标签 1, 标签 2
---

# 正文内容
MARKDOWN

# 发布文章
python3 scripts/publish_post.py --file articles/my-post.md

# 保存为草稿
python3 scripts/publish_post.py --file articles/my-post.md --draft
```
