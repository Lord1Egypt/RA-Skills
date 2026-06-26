# Save to Obsidian

将网页文章保存到 Obsidian 知识库，自动完成摘要、标签、图片本地化。

## 功能特性

- ✅ **批量处理**：支持一次处理多个文章链接
- ✅ **多源抓取**：微信公众号、知乎、掘金、Medium、博客等
- ✅ **智能摘要**：自动生成结构化摘要（核心观点 + 关键要点 + 适用场景）
- ✅ **自动标签**：从内容提取相关标签（技术领域 + 主题类型）
- ✅ **图片本地化**：自动下载图片，使用相对路径引用
- ✅ **去重检测**：基于 URL 自动跳过已保存的文章
- ✅ **失败重试**：网络失败自动重试 3 次
- ✅ **用户笔记**：支持添加个人笔记

## 安装

1. 下载 skill 文件
2. 修改脚本中的路径配置：
   ```python
   OBSIDIAN_DIR = os.path.expanduser("~/Documents/Obsidian/Articles")
   ATTACHMENTS_DIR = os.path.expanduser("~/Documents/Obsidian/attachments")
   ```
3. 确保系统已安装 Python 3.7+ 和 curl

## 使用方法

### 命令行

```bash
# 单篇文章
python3 save_article_to_obsidian.py "https://mp.weixin.qq.com/s/xxx"

# 多篇文章
python3 save_article_to_obsidian.py \
  "https://mp.weixin.qq.com/s/xxx" \
  "https://zhuanlan.zhihu.com/p/yyy" \
  "https://example.com/article"

# 带笔记
python3 save_article_to_obsidian.py "https://..." "这是我的笔记"
```

## 输出格式

```markdown
---
title: "文章标题"
url: "https://..."
created: 2026-04-07
source: wechat
tags:
  - ai
  - security
  - tutorial
---

## 📌 摘要

**核心观点**: 文章核心内容概述...

**关键要点**:
- 要点 1
- 要点 2
- 要点 3

**适用场景**: 目标读者群体

🔗 [阅读原文](https://...)

## 💭 我的笔记（可选）

> 用户添加的笔记
^note-xxx

---

正文内容...
```

## 技术亮点

| 特性 | 说明 |
|------|------|
| 懒加载图片处理 | 优先提取 `data-src` 属性获取真实图片地址 |
| 双通道抓取 | Jina Reader → curl fallback |
| 智能内容解析 | 自动识别文章结构，提取关键信息 |
| 并发安全 | 单线程顺序处理，避免资源冲突 |

## 依赖

- Python 3.7+
- curl

## License

MIT
