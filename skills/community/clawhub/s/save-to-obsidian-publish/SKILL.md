# Save to Obsidian

Save web articles to Obsidian knowledge base with auto-generated summaries, tags, and local image storage.

## Features

- ✅ **Batch Processing**: Process multiple article links at once
- ✅ **Multi-source Support**: WeChat, Zhihu, Juejin, Medium, blogs, etc.
- ✅ **Smart Summary**: Auto-generate structured summary (core idea + key points + audience)
- ✅ **Auto Tags**: Extract relevant tags (tech domain + topic type)
- ✅ **Image Localization**: Download images locally with relative paths
- ✅ **Duplicate Detection**: Skip already saved articles based on URL
- ✅ **Retry on Failure**: Auto-retry 3 times on network failure
- ✅ **User Notes**: Support adding personal notes

## ⚠️ Mandatory Rules

### Image Paths — Relative Only

All images in the saved Markdown **MUST** use **relative paths**, never absolute URLs.

- ✅ Correct: `![图片](../attachments/{hash}/{filename}.png)`
- ❌ Wrong: `![图片](https://mmbiz.qpic.cn/...)`
- ❌ Wrong: `![图片](/absolute/path/to/attachments/...)`

The script handles this automatically. If you process articles manually (e.g., due to anti-scraping), you **must**:
1. Download each image to `ATTACHMENTS_DIR/{article_hash}/`
2. Replace the URL with `../attachments/{article_hash}/{filename}`
3. Verify images were actually saved (file size > 100 bytes)

This ensures Obsidian can display images offline and iCloud sync works correctly.

## Usage

```bash
# Single article
python3 save_article_to_obsidian.py "https://mp.weixin.qq.com/s/xxx"

# Multiple articles
python3 save_article_to_obsidian.py \
  "https://mp.weixin.qq.com/s/xxx" \
  "https://zhuanlan.zhihu.com/p/yyy"

# With notes
python3 save_article_to_obsidian.py "https://..." "My notes here"
```

## Output Format

```markdown
---
title: "Article Title"
url: "https://..."
created: 2026-04-07
source: wechat
tags:
  - ai
  - security
  - tutorial
---

## 📌 Summary

**Core Idea**: Article summary...

**Key Points**:
- Point 1
- Point 2
- Point 3

**Audience**: Target readers

🔗 [Read Original](https://...)

---

Article content...
```

## Installation

1. Download the skill files
2. Configure paths in the script:
   ```python
   OBSIDIAN_DIR = os.path.expanduser("~/Documents/Obsidian/Articles")
   ATTACHMENTS_DIR = os.path.expanduser("~/Documents/Obsidian/attachments")
   ```
3. Ensure Python 3.7+ and curl are installed

## Dependencies

- Python 3.7+
- curl

## License

MIT
