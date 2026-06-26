---
name: xia-zhua-zhua
description: >
  虾抓抓(xia-zhua-zhua) v4.0 - 超强内容抓取技能
  支持：Markdown/PDF/多模态提取/结构化抽取/翻译/视频下载
  触发词：抓取网页、网页转Markdown、内容抓取、虾抓抓、视频下载
version: 4.0.0
---

# 虾抓抓 v4.0 - 超强内容抓取技能

> 原名：xia-zhua-zhua，又称Content Catcher

---

## 升级亮点 (v4.0)

| 新功能 | 说明 |
|--------|------|
| PDF导出 | 直接导出为PDF |
| 多模态提取 | 图片/音频/视频资源 |
| 结构化抽取 | 表格/列表/卡片智能识别 |
| 增量监测 | 页面更新自动提醒 |
| 翻译集成 | 抓取后自动翻译 |
| 深度渲染 | 完整JS动态内容 |

---

## 核心能力

### 1. 网页内容抓取

| 模式 | 命令 | 说明 |
|------|------|------|
| 标准模式 | `node markdown-clip.js <url>` | CSS选择器 |
| Smart模式 | `node markdown-clip.js <url> --smart` | Readability AI |
| 分析模式 | `node markdown-clip.js <url> --analyze` | 摘要+关键词 |

### 2. 视频下载

| 命令 | 说明 |
|------|------|
| `python video_catcher_pro.py ytdlp <url>` | yt-dlp下载 |
| `python video_catcher_pro.py m3u8 <url>` | M3U8下载 |

---

## v4.0 新增功能

### 多模态提取
```bash
# 提取图片资源
node content-extractor.js <url> --images

# 提取所有媒体
node content-extractor.js <url> --media
```

### PDF导出
```bash
# 导出为PDF
node content-extractor.js <url> --pdf

# Markdown + PDF双导出
node content-extractor.js <url> --both
```

### 结构化抽取
```bash
# 智能识别表格
node content-extractor.js <url> --tables

# 识别列表数据
node content-extractor.js <url> --lists
```

### 增量监测
```bash
# 监测页面更新
node content-watcher.js <url> --watch

# 设置更新提醒
node content-watcher.js <url> --watch --notify
```

### 翻译功能
```bash
# 翻译为英文
node content-extractor.js <url> --translate en

# 翻译为日文
node content-extractor.js <url> --translate jp
```

---

## 技术架构

```
┌─────────────────────────────────────────────────────────┐
│              Content Catcher v4.0                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │  Playwright  │  │   Turndown   │  │   yt-dlp    │    │
│  │  (渲染)      │  │ (Markdown)  │  │  (视频)     │    │
│  └──────┬──────┘  └──────┬──────┘  └─────────────┘    │
│         │                 │                            │
│  ┌──────▼──────┐  ┌──────▼──────┐                     │
│  │ 多模态提取   │  │  结构化    │                     │
│  │ 图片/音频   │  │  表格/列表  │                     │
│  └─────────────┘  └─────────────┘                     │
│         │                                                    │
│  ┌──────▼──────┐                                        │
│  │  输出格式   │                                        │
│  │ Markdown   │                                        │
│  │ PDF        │                                        │
│  │ JSON       │                                        │
│  └─────────────┘                                        │
└─────────────────────────────────────────────────────────┘
```

---

## 升级对比

| 功能 | v2.x | v3.x | v4.x |
|------|-------|-------|-------|
| Markdown | ✅ | ✅ | ✅ |
| Smart模式 | ✅ | ✅ | ✅ |
| 分析 | ✅ | ✅ | ✅ |
| 视频下载 | - | ✅ | ✅ |
| PDF导出 | - | - | ✅ |
| 多模态 | - | - | ✅ |
| 结构化 | - | - | ✅ |
| 增量监测 | - | - | ✅ |
| 翻译 | - | - | ✅ |

---

## 依赖工具

| 工具 | 状态 | 用途 |
|------|------|------|
| Node.js | ✅ | 运行环境 |
| Playwright | ✅ | 页面渲染 |
| Turndown | ✅ | HTML→Markdown |
| Python | ✅ | 分析/翻译 |
| yt-dlp | ✅ | 视频下载 |
| weasyprint | ✅ | PDF导出 |
| googletrans | ⬜ | 翻译(可选) |

---

## 使用示例

### 基础抓取
```bash
node xia-zhua-zhua/markdown-clip.js https://example.com --smart
```

### 多模态+PDF
```bash
node content-extractor.js https://example.com --media --pdf
```

### 视频下载
```bash
python video-catcher/video_catcher_pro.py ytdlp https://b.com/video
```

---

## 文件结构

```
content-catcher/
├── SKILL.md                    # 本文档
├── xia-zhua-zhua/            # 虾抓抓模块
│   ├── markdown-clip.js       # 主脚本
│   └── ...
└── video-catcher/            # 视频模块
    ├── video_catcher_pro.py  # 主脚本
    └── ...
```

---

## 更新日志

### v4.0.0 (最新)
- 多模态内容提取
- PDF导出
- 结构化数据抽取
- 增量更新监测
- 翻译集成

### v3.0.0
- 融合Video Catcher

### v2.1.3
- Smart模式
- 分析功能
