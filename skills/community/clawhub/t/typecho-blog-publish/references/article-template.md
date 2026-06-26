# 示例文章模板

## 使用方法

1. 复制此文件，修改内容
2. 修改头部信息（title, categories, tags）
3. 运行发布命令

## 发布命令

```bash
# 保存为草稿
python3 ../../scripts/publish_post.py --file my-article.md --draft

# 直接发布
python3 ../../scripts/publish_post.py --file my-article.md
```

---

## 文章格式示例

```markdown
---
title: 你的文章标题
categories: 分类 1, 分类 2
tags: 标签 1, 标签 2
---

# 文章正文

这里是内容...
```
