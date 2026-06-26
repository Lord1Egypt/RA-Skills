# Typecho 博客发布技能 v2.0 - 使用指南

## 📋 技能概述

**版本**: v2.0  
**状态**: ✅ 已封装  
**功能**: 根据主题自动生成带配图的博客草稿  
**特点**: 
- 支持手动指定精准配图（推荐）
- 支持自动搜索配图（备选）
- 自动上传到 Typecho 服务器
- 发布为草稿，待预览后手动发布

---

## 🎯 使用方法

### 方式 1: 手动指定配图 URL（推荐⭐）

**适用场景**: 对配图有精准要求，确保图片与主题高度相关

```bash
cd /home/jiliang/.openclaw/workspace/skills/typecho-blog-publish/scripts

# 语法
python3 publish_v2_full.py "文章主题" "分类" "标签 1，标签 2" --image "图片 URL"

# 示例 1: AI 主题 + Pexels 图片
python3 publish_v2_full.py "AI 如何改变我们的生活" "AI" "人工智能，生活，科技" \
  --image "https://images.pexels.com/photos/373543/pexels-photo-373543.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"

# 示例 2: 科技主题
python3 publish_v2_full.py "2026 年科技趋势" "技术" "科技，未来" \
  --image "https://images.pexels.com/photos/118152/pexels-photo-118152.jpeg"
```

**配图来源推荐**:
- Pexels: https://www.pexels.com/search/ai%20technology/
- Pixabay: https://pixabay.com/images/search/artificial%20intelligence/
- Unsplash: https://unsplash.com/s/photos/artificial-intelligence

---

### 方式 2: 使用本地图片文件

**适用场景**: 已有本地截图或图片文件

```bash
# 语法
python3 publish_v2_full.py "文章主题" "分类" "标签" --image-file "/path/to/image.png"

# 示例
python3 publish_v2_full.py "AI 实战指南" "AI" "人工智能" \
  --image-file "/home/jiliang/workspace/screenshot.png"
```

---

### 方式 3: 自动搜索配图（不推荐）

**适用场景**: 对配图要求不高，接受随机图片

```bash
# 语法
python3 publish_v2_full.py "文章主题" "分类" "标签"

# 示例
python3 publish_v2_full.py "AI 改变生活" "AI" "人工智能"
```

**注意**: 自动搜索的图片来自 LoremFlickr，质量参差不齐，可能与主题不够匹配。

---

## 📊 完整工作流程

```
1. 准备阶段
   - 确定文章主题
   - 准备配图（从 Pexels 等找图，或准备本地图片）
   ↓
2. 执行发布
   - 调用脚本（指定图片 URL）
   ↓
3. 自动处理
   - 下载/读取图片
   - 上传到 Typecho 服务器
   - 获取真实 URL
   - 生成 Markdown 文案
   - 发布为草稿
   ↓
4. 预览检查
   - 访问草稿链接
   - 检查标题、配图、分类、标签
   ↓
5. 手动发布
   - 确认无误后点击"发布"
   - 或修改后发布
```

---

## 🛠️ 核心功能

### 1. 图片处理
- ✅ 支持网络图片 URL
- ✅ 支持本地图片文件
- ✅ 自动上传到 Typecho
- ✅ 获取真实 URL（非相对路径）
- ✅ 插入到 Markdown 文案开头

### 2. 文案生成
- ✅ 自动生成标题、引言、正文、总结
- ✅ 自动添加 YAML 头部
- ✅ 自动插入配图（带描述）
- ✅ Markdown 格式（自动转 HTML）

### 3. 分类匹配
- ✅ 自动获取博客已有分类
- ✅ 智能匹配输入分类
- ✅ 完全匹配优先，模糊匹配备选

### 4. 发布模式
- ✅ 默认草稿模式（安全）
- ✅ 可手动发布
- ✅ 可预览检查

---

## 📝 文案模板结构

```markdown
---
title: AI 如何改变我们的生活
categories: AI
tags: 人工智能，生活，科技
---

# AI 如何改变我们的生活

> **摘要**：本文探讨 AI 如何改变我们的生活的相关内容，带你了解最新趋势和实用技巧。

![AI 如何改变我们的生活配图 1](http://yuanblog.tk:9980/usr/uploads/2026/04/xxx.jpeg)

## 引言

AI 如何改变我们的生活是当下热门话题...

## 核心观点

1. **观点一**：详细内容...
2. **观点二**：详细内容...
3. **观点三**：详细内容...

## 实际应用

- 场景一：...
- 场景二：...
- 场景三：...

## 总结

...
```

---

## ⚠️ 注意事项

### 配图相关
- ✅ 推荐手动指定高质量图片（Pexels/Pixabay）
- ✅ 图片尺寸建议：1200x630 或更大
- ✅ 图片格式：JPG/PNG
- ❌ 避免使用过小的图片
- ❌ 避免使用有版权的图片

### 分类相关
- ✅ 使用已有分类名称（如"AI"、"技术"）
- ⚠️ 分类不匹配时会尝试模糊匹配
- ⚠️ 完全无法匹配时归入 default

### 发布相关
- ✅ 默认发布为草稿（安全）
- ✅ 必须预览检查后再发布
- ✅ 检查配图是否显示正常
- ❌ 不要跳过预览直接发布

---

## 🔧 技术细节

### 文件结构
```
skills/typecho-blog-publish/
├── scripts/
│   ├── publish_v2_full.py    # v2.0 主脚本（推荐）
│   ├── publish_post.py       # 基础发布模块
│   ├── image_finder.py       # 图片搜索模块
│   └── upload_image.py       # 图片上传模块
├── SKILL.md                  # 技能说明
├── README_V2.md              # 本文档
└── articles/                 # 示例文章
```

### 依赖
- Python 3.x
- xmlrpc.client
- requests
- 博客配置（.env 文件）

### 配置要求
`.env` 文件需包含：
```bash
BLOG_URL=http://yuanblog.tk:9980
BLOG_USERNAME=admin
BLOG_PASSWORD=你的密码
BLOG_XMLRPC=/index.php/action/xmlrpc
```

---

## 📊 测试记录

| 测试日期 | 文章 ID | 主题 | 配图方式 | 结果 |
|---------|--------|------|---------|------|
| 2026-04-03 | 996 | AI 如何改变生活 | 自动搜索 | ⚠️ 分类默认 |
| 2026-04-03 | 998 | AI 如何改变生活 | 自动搜索 | ✅ 分类匹配 |
| 2026-04-03 | 1001 | AI 如何改变生活 | 自动搜索 | ⚠️ 分类 default |
| 2026-04-03 | 1003 | AI 如何改变生活 | 手动指定 | ✅ 配图精准 |

---

## 🚀 最佳实践

### 推荐流程
1. **找图**: 从 Pexels 搜索与主题匹配的图片
2. **复制链接**: 右键图片→复制图片地址
3. **发布草稿**: 使用 `--image` 参数指定图片 URL
4. **预览检查**: 访问草稿链接，检查配图、分类、内容
5. **手动发布**: 确认无误后点击发布

### 配图选择技巧
- **主题相关**: AI 主题选 AI 相关图片，科技主题选科技图片
- **高质量**: 选择清晰、专业的图片
- **尺寸合适**: 至少 1200x630，避免小图
- **版权安全**: 使用 Pexels/Pixabay 等免费图库

---

## 📚 相关文档

- `SKILL.md` - 技能详细说明
- `CHECKLIST.md` - 发布检查清单
- `PUBLISH.md` - 发布流程详解
- `SUMMARY.md` - 技能总结

---

*维护者：团子 🌟*  
*版本：v2.0*  
*更新时间：2026-04-03 10:50*  
*状态：✅ 已封装，待最终确认*
