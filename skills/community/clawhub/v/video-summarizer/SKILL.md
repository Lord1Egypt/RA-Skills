---
name: video-summarizer
description: "将 B 站/YouTube/小红书/抖音视频转换为结构化 Notion 总结文档，自动上传截图，一键推送 Notion"
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires": { "bins": ["ffmpeg (>=6.1)", "yt-dlp (>=2026.03.17)"], "env": ["LLM_API_KEY", "LLM_BASE_URL", "ALIYUN_OSS_AK", "ALIYUN_OSS_SK", "ALIYUN_OSS_BUCKET_ID", "ALIYUN_OSS_ENDPOINT"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "ffmpeg yt-dlp",
              "bins": ["ffmpeg", "yt-dlp"],
              "label": "Install ffmpeg and yt-dlp (brew)",
            },
            {
              "id": "apt",
              "kind": "apt",
              "packages": "ffmpeg yt-dlp",
              "bins": ["ffmpeg", "yt-dlp"],
              "label": "Install ffmpeg and yt-dlp (apt)",
            },
            {
              "id": "pip",
              "kind": "pip",
              "packages": "requests==2.31.0 oss2==2.18.4 python-dotenv==1.0.1 biliup==0.4.86",
              "label": "Install Python dependencies",
            },
          ],
      },
  }
---

# Video Summarizer — OpenClaw Skill

将 B 站/YouTube/小红书/抖音视频转换为结构化 Notion 总结文档，自动上传截图，一键推送 Notion。

**版本**: 1.0.13  
**发布**: 2026-05-10  
**许可**: MIT  
**作者**: Ajay Hao

---

> ⚠️ **安全提示**
> - 本技能会将视频内容发送至第三方 AI 服务进行分析
> - 建议使用专用 API Key（非生产环境）
> - OSS Bucket 请配置最小权限（仅写入/读取）
> - B 站 Cookies 仅在你控制的设备上使用

---

## 📖 技能描述

### 核心能力

- 🎬 **多平台支持**: B 站、YouTube、小红书、抖音
- 📝 **智能分析**: AI（平台可配置）提取关键概念、核心要点、注意事项
- 📸 **截图嵌入**: 基于 AI 分析结果自动生成关键帧截图
- ☁️ **图床集成**: 阿里云 OSS 自动上传，永久链接
- 🚀 **一键推送**: 自动推送 Notion 数据库

### 技术特性

- **双模式转录**: Plan A（官方字幕）优先，Plan B（语音转录）兜底
- **并行优化**: 字幕下载与视频下载并行执行，节省 32% 时间
- **GPU 自适应**: 自动检测显存，选择最优 Whisper 模型
- **断点续跑**: 支持从中断点恢复，避免重复处理
- **四层标签**: 标题 hashtag → 元数据 → AI 关键词 → 默认值

---

## 🔐 安全与隐私说明

### 敏感数据处理

| 文件/路径 | 用途 | 敏感性 | 用户控制 |
|-----------|------|--------|----------|
| `~/.cookies/bilibili_cookies.txt` | B 站官方字幕获取 | 高（Session Token） | 用户主动扫码生成，可随时删除 |
| `~/.openclaw/.env` | API Keys 存储 | 高 | 用户自行配置，skill 不修改 |
| `/tmp/video-summarizer-*/` | 临时输出 | 低 | 处理完成后可手动清理 |

### 外部服务端点

| 服务 | 域名 | 用途 | 传输数据 |
|------|------|------|----------|
| LLM 平台 (可配置) | 通过 LLM_BASE_URL 指定 | AI 分析 | 字幕文本、元数据 |
| 阿里云 OSS | `oss-cn-shanghai.aliyuncs.com` | 图床上传 | 截图、封面图 |
| Groq | `api.groq.com` | 备用转录（可选，需代理） | 音频片段 |
| Bilibili | `bilibili.com` | 视频下载/字幕 | 无（仅下载） |
| YouTube | `youtube.com` | 视频下载/字幕 | 无（仅下载） |
| 抖音 | `douyin.com` / `iesdouyin.com` | 视频下载 | 无（仅下载） |

**说明**: 
- LLM 平台由用户通过 `LLM_BASE_URL` 控制，支持任意 OpenAI 兼容接口（DeepSeek / DashScope / OpenAI / Groq 等）
- Groq API 为可选加速方案，未配置时自动降级到本地 Faster-Whisper
- 抖音专用下载器 `douyin_downloader.py` 已移除硅基流动依赖，使用与主流程一致的 Groq API + 本地降级方案

### 最小权限建议

- **OSS Bucket**: 创建专用 Bucket，仅授予 PutObject/GetObject 权限
- **API Keys**: 使用子账号 Key，设置 IP 白名单
- **测试环境**: 首次使用建议在隔离环境测试

### ⚠️ 数据流向提醒

- **LLM 平台（可配置）**: 字幕文本和视频元数据会发送至用户配置的 LLM 服务（通过 `LLM_BASE_URL` 指定），请勿处理包含敏感信息的视频
- **Groq（可选）**: 音频片段会发送至 Groq API（加速转录），未配置时自动降级为本地 Faster-Whisper
- **阿里云 OSS**: 截图和封面图上传至 OSS Bucket，建议配置为专用 Bucket 并设置为私有读/写
- **Notion**: 总结结果推送至 Notion 数据库，确保 Integration 仅授予目标数据库权限
- **B 站 Cookies**: 扫码登录后存储于 `~/.cookies/bilibili_cookies.txt`，权限已限制为 600，仅限本机访问
- **Cookie 安全**: 登录完成后临时 `cookies.json` 会自动清理，不残留 skill 目录内

---

## 🎯 平台支持详情

### Bilibili（完整支持）

**字幕**: ✅ 官方字幕 + 自动字幕  
**语音转录**: ✅ 支持（Plan B）  
**Cookies**: 推荐（获取官方字幕）  
**下载工具**: yt-dlp (>=2026.03.17)

#### 操作步骤

```bash
# 1. 扫码登录（首次使用，获取官方字幕）
cd ~/.openclaw/skills/video-summarizer/scripts
./bili-login.sh

# 2. 处理视频
./video-summarize.sh "https://www.bilibili.com/video/BV1xxxx"

# 3. 查看结果
cat /tmp/video-summarizer-*/summary.md
```

**说明**:
- Cookies 文件：`~/.cookies/bilibili_cookies.txt`
- 无 Cookies 时使用 Plan B 语音转录
- 支持 b23.tv 短链

---

### YouTube（完整支持）

**字幕**: ✅ 自动字幕（多语言）  
**语音转录**: ✅ 支持（Plan B）  
**Cookies**: ❌ 不需要  
**下载工具**: yt-dlp (>=2026.03.17)

#### 操作步骤

```bash
# 直接处理（无需登录）
./video-summarize.sh "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# 指定输出目录
./video-summarize.sh "https://youtu.be/dQw4w9WgXcQ" /tmp/output
```

**说明**:
- 需网络可达（可能需要代理）
- 优先下载英文字幕，无则用语音转录
- 支持 youtu.be 短链

---

### 小红书（基本支持）

**字幕**: ❌ 无字幕  
**语音转录**: ✅ 唯一方式（Plan B）  
**Cookies**: ❌ 不需要  
**下载工具**: yt-dlp (>=2026.03.17)

#### 操作步骤

```bash
# 直接处理（自动使用 Plan B 语音转录）
./video-summarize.sh "https://www.xiaohongshu.com/explore/xxxx"

# 或短链
./video-summarize.sh "https://xhslink.com/o/xxxx"
```

**说明**:
- 必须使用 Plan B 语音转录
- 推荐配置 GROQ_API_KEY 加速转录
- 自动上传封面图到 OSS

---

### 抖音（完整支持）

**字幕**: ❌ 无字幕  
**语音转录**: ✅ 唯一方式（Plan B）  
**Cookies**: ❌ 不需要（专用下载器）  
**下载工具**: douyin_downloader.py

#### 操作步骤

```bash
# 直接处理（专用下载器，无需 Cookies）
./video-summarize.sh "https://www.douyin.com/video/7234567890"

# 支持短链
./video-summarize.sh "https://v.douyin.com/abc123/"
```

**说明**:
- 使用专用下载器 `douyin_downloader.py`（仅用于获取元数据和下载视频）
- 无反爬限制，无需 Cookies
- 语音转录使用主流程的 `transcribe-audio.py`（Groq API + 本地降级）
- `douyin_downloader.py` 的 extract 模式已移除硅基流动依赖，改用 Groq API + 本地降级

---

## ⚙️ 配置详解

### 环境变量（~/.openclaw/.env）

```bash
# ========== 必需配置 ==========

# LLM AI 分析（OpenAI 兼容接口，三者缺一不可）
LLM_API_KEY=sk-your-api-key
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-v4-pro

# 其他平台示例：
# LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1  # DashScope
# LLM_BASE_URL=https://api.openai.com/v1                          # OpenAI
# LLM_BASE_URL=https://api.groq.com/openai/v1                     # Groq

# 阿里云 OSS 图床
ALIYUN_OSS_AK=your_access_key_id
ALIYUN_OSS_SK=your_access_key_secret
ALIYUN_OSS_BUCKET_ID=your_bucket_name
ALIYUN_OSS_ENDPOINT=oss-cn-shanghai.aliyuncs.com

# ========== 可选配置 ==========

# Notion 自动推送（可选）
NOTION_API_KEY=<your_notion_api_key>
NOTION_VIDEO_SUMMARY_DATABASE_ID=<your_database_id>  # 单个数据库 ID

# 语音转录加速（Groq API，可选）
# 国内需代理访问，如未配置自动降级到本地 Faster-Whisper
# 不配置此项不影响使用
# 注意：douyin_downloader.py 也使用此变量（已移除硅基流动依赖）
GROQ_API_KEY=<your_groq_api_key>

# 本地 Whisper 模型（有 GPU 时自动检测）
WHISPER_MODEL=base  # tiny/base/small/medium/large
```

### OSS Bucket 要求

- **访问权限**: 公开可读（直接 URL 访问）
- **CORS 配置**: 允许跨域访问（Notion 嵌入需要）
- **存储类型**: 标准存储（低频访问会影响加载速度）

### Notion 数据库配置

#### 数据库属性（Properties）

| 属性名 | 类型 | 说明 | 来源 |
|--------|------|------|------|
| **Title** | `title` | 视频标题（≤200 字符） | Markdown `# 标题` |
| **Source** | `rich_text` | 平台来源（Bilibili/YouTube/小红书/抖音） | metadata.platform / URL 推断 |
| **Author** | `rich_text` | UP 主/作者名称 | Markdown `**UP 主:**` / metadata.uploader |
| **Url** | `url` | 视频原始链接 | metadata.webpage_url / Markdown `**链接:**` |
| **Tags** | `multi_select` | 标签（最多 5 个） | 三层策略提取 |
| **PubDate** | `date` | 发布日期 | metadata.upload_date |
| **Length** | `rich_text` | 视频时长（MM:SS 格式） | metadata.duration_string |
| **Cover** | `files` | 封面图片（可选，外部 URL） | metadata.thumbnail |
| **ts** | `date` | 创建时间戳（ISO 8601，东八区 +08:00） | 当前时间 |

#### 配置步骤

1. **创建数据库**（Table 视图）

2. **添加上述 9 个属性**（字段名必须完全匹配）

3. **获取 Database ID**：
   - 打开数据库 → 复制 URL 中 `?v=` 后的 ID
   - 示例：`https://notion.so/your-workspace/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx?v=yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy`
   - Database ID = `yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy`

4. **配置环境变量**：
   ```bash
   NOTION_API_KEY=<your_notion_api_key>
   NOTION_VIDEO_SUMMARY_DATABASE_ID=<your_database_id>  # 单个数据库
   ```

#### 数据库视图示例

```
┌─────────┬──────────┬─────────┬──────┬──────┬─────────┬────────┬───────┬─────────────┐
│ Title   │ Source   │ Author  │ Url  │ Tags │ PubDate │ Length │ Cover │ ts          │
│ title   │ text     │ text    │ url  │ multi│ date    │ text   │ files │ date        │
└─────────┴──────────┴─────────┴──────┴──────┴─────────┴────────┴───────┴─────────────┘
```

---

## 🏗️ 系统架构

### 处理流程

```
用户输入 (视频 URL)
       ↓
Step 1: 平台识别 + 元数据
       ↓
┌──────┴──────┐
↓             ↓
Step 2: 字幕   Step 3: 视频下载  ← 并行执行
       ↓             ↓
       └──────┬──────┘
              ↓
Step 4: 文本提取 (VTT → TXT / Plan B 转录)
       ↓
Step 5: AI 分析 (OpenAI 兼容接口，通过 LLM_API_KEY + LLM_BASE_URL + LLM_MODEL 配置)
       ↓
Step 6: 截图生成 (ffmpeg, 基于 AI 时间戳)
       ↓
Step 7: OSS 上传 (截图 + 封面)
       ↓
Step 8: Markdown 渲染
       ↓
Step 9: Notion 推送 (可选)
```

### 技术栈

| 层级 | 技术 |
|------|------|
| 编排层 | Bash (video-summarize.sh) |
| 分析层 | Python + OpenAI 兼容 LLM API |
| 转录层 | Groq API (可选) / Faster-Whisper (本地) |
| 工具层 | yt-dlp (>=2026.03.17), ffmpeg (>=6.1), oss2, requests |

### 数据文件

| 文件 | 来源 | 用途 |
|------|------|------|
| `metadata.json` | yt-dlp / douyin_downloader | 视频元数据 |
| `transcript.txt` | VTT 提取 / Plan B 转录 | 纯文本字幕 |
| `ai_result.json` | analyze-subtitles-ai.py | AI 分析结果 |
| `screenshot_urls.txt` | upload-to-oss.py | 截图 OSS 链接 |
| `summary.md` | analyze-subtitles-ai.py | 最终总结 |

---

## 📋 脚本清单

### 核心脚本（4 个）

| 脚本 | 功能 |
|------|------|
| `video-summarize.sh` | 主流程编排（Plan A/B 自动选择） |
| `analyze-subtitles-ai.py` | AI 分析 + Markdown 渲染 |
| `upload-to-oss.py` | OSS 图床上传（截图 + 封面） |
| `push-to-notion.py` | Notion 推送（优先使用环境变量 `NOTION_VIDEO_SUMMARY_DATABASE_ID`，其次 CLI 参数） |

### 平台工具（2 个）

| 脚本 | 功能 |
|------|------|
| `bili-login.sh` | B 站扫码登录（获取 Cookies） |
| `douyin_downloader.py` | 抖音专用下载器（无需 Cookies，info/download 操作无需 API；extract 模式使用 Groq API + 本地降级转录音频） |

### 辅助工具（4 个）

| 脚本 | 功能 |
|------|------|
| `download-audio.sh` | Plan B: 音频下载 |
| `transcribe-audio.py` | Plan B: 语音转录（GPU 自适应） |
| `check-config.sh` | 配置检查 |
| `convert-bili-cookie.py` | Cookies 格式转换 |

---

## 🎯 Plan A vs Plan B

### 对比表

| 项目 | Plan A | Plan B |
|------|--------|--------|
| **字幕来源** | 平台官方字幕 | 语音转录 |
| **准确率** | 90%+ | 80-90% |
| **速度** | 快 (1-2 分钟) | 较慢 (3-5 分钟) |
| **依赖** | Cookies（B 站） | GPU 或 API Key |

### 各平台使用情况

| 平台 | Plan A | Plan B | 默认 |
|------|--------|--------|------|
| **Bilibili** | ✅ 官方 + 自动 | ✅ 备用 | Plan A |
| **YouTube** | ✅ 自动字幕 | ✅ 备用 | Plan A |
| **小红书** | ❌ 无 | ✅ 唯一 | Plan B |
| **抖音** | ❌ 无 | ✅ 唯一 | Plan B |

### Plan B 三层降级方案

```
1. Groq API (whisper-large-v3) → 云端高速（可选，需配置 GROQ_API_KEY 且网络可达）
   └─ 失败/未配置 → 降级到本地

2. Faster-Whisper (本地) → GPU/CPU 自适应
   ├─ GPU ≥8GB  → large-v2 模型
   ├─ GPU ≥4GB  → medium 模型
   ├─ GPU ≥2GB  → small 模型
   ├─ GPU ≥1GB  → base 模型 (GPU)
   └─ 无 GPU    → base 模型 (CPU)
   └─ 失败 → 降级到方案 3

3. Whisper.cpp / OpenAI Whisper (本地保底)
   └─ 完全离线，作为最终兜底
```

**说明**: 
- Groq API 为可选配置，未配置时直接使用本地 Faster-Whisper
- 本地转录无需任何 API Key，完全离线运行
- 国内使用 Groq 需配置代理
- **抖音专用下载器** `douyin_downloader.py` 也使用 Groq API + 本地降级方案（已移除硅基流动依赖），extract 模式用于音频转录

---

## 📁 输出文件结构

```
output/
├── summary.md              # 📝 最终总结（主要成果）
├── ai_result.json          # 🧠 AI 分析原始结果（结构化 JSON）
├── screenshot_urls.txt     # 🔗 截图 OSS 链接
├── metadata.json           # 📊 视频元数据
├── transcript.txt          # 📄 纯文本字幕
├── audio.txt               # 🎤 语音转录原始文本（Plan B 时使用）
├── cover_url.txt           # ☁️ 封面 OSS 上传结果
├── screenshot_times.txt    # ⏱️ 截图时间戳记录
├── screenshots/            # 📸 截图原图（本地备份）
├── cover.jpg              # 🖼️ 封面图（本地备份）
└── *.log                   # 📋 日志文件（verbose 模式）
```

### OSS 路径规范

**截图路径**: `/screenshots/<平台>/<视频 ID>_<时间戳>/<截图文件>`

```
screenshots/bilibili/BV1eTPEzNEqf_20260405_053203/screenshot_01.jpg
screenshots/douyin/7234567890_20260405_175010/chapter_01.jpg
screenshots/xhs/69c1493b000000002003b3ce_20260405_152852/screenshot_01.jpg
screenshots/youtube/dQw4w9WgXcQ_20260405_120000/screenshot_01.jpg
```

**封面路径**: `thumbnails/<平台>/<视频 ID>/cover.jpg`

```
thumbnails/bilibili/BV1eTPEzNEqf/cover.jpg
thumbnails/douyin/7234567890/cover.jpg
```

---

## 🏷️ 标签策略

### 四层提取策略

```
1. 标题 hashtag → #([\w\u4e00-\u9fa5]+)
   示例："#AI 教程 #大模型原理" → ["AI 教程", "大模型原理"]

2. 元数据 tags → yt-dlp 提取的原始标签
   示例：["原理", "AI", "教程", "claude", "大模型"]

3. AI 关键词 → AI 分析提取的核心概念
   示例：["Transformer", "注意力机制", "深度学习"]

4. 默认值 → 视频总结/知识分享/学习
   当前三层都为空时使用
```

### 标签规则

- **长度**: 2-15 字符（兼容英文如 "openclaw"）
- **数量**: 最多 5 个
- **去重**: 自动去重，保留唯一值
- **优先级**: 1 → 2 → 3 → 4

---

## 🔧 故障排查

### Cookies 过期（B 站）

```bash
# 重新扫码登录
./bili-login.sh
```

### 配置检查

```bash
# 运行检查脚本
./check-config.sh
```

### 查看详细日志

```bash
# 使用 verbose 模式
./video-summarize.sh "URL" --verbose

# 查看错误日志
cat /tmp/output/error.log
```

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 截图 404 | OSS 路径不匹配 | `python3 upload-to-oss.py auto /tmp/output` |
| 标签默认值 | 标签提取失败 | 检查标题 hashtag 格式 `#标签` |
| 转录失败 | 无 GPU/API 配额 | 检查 `GROQ_API_KEY`，或确保 `faster-whisper` 已安装 |
| Notion 推送失败 | API Key 过期 | 更新 `NOTION_API_KEY`（可选功能，仅 --push 需要） |
| 并行任务失败 | 依赖缺失 | 检查 `ffmpeg` / `yt-dlp` 安装（版本要求：ffmpeg >= 6.1, yt-dlp >= 2026.03.17） |
| 抖音下载失败 | 链接格式错误 | 使用完整 URL 或 v.douyin.com 短链 |
| 抖音文案提取失败 | 无 API Key | `douyin_downloader.py` 会自动降级到本地 Faster-Whisper，无需单独配置 |

---

## 📊 性能基准

### 处理时间（10 分钟视频）

| 平台 | Plan A | Plan B（本地） | Plan B（Groq） |
|------|--------|----------------|----------------|
| **Bilibili** | ~90 秒 | ~150 秒 | ~120 秒 |
| **YouTube** | ~90 秒 | ~150 秒 | ~120 秒 |
| **小红书** | - | ~150 秒 | ~120 秒 |
| **抖音** | - | ~150 秒 | ~120 秒 |

**优化效果**: 并行优化后节省约 30 秒（32%↓）

---

## 📝 输出格式（summary.md）

1. **标题 + Tags + Author**
2. **📝 Note** — AI 概述（150-250 字）
3. **📺 视频信息** — 链接/时长/播放数据
4. **📚 关键概念** — 术语表格（3-5 个，按时间排序）
5. **🎯 核心要点** — emoji+ 描述 + 时间戳（5-8 个）
6. **🎬 视频章节** — 标题 + 时间轴 + 截图
7. **⚠️ 注意事项** — 特别提醒（2-4 个）
8. **💡 总结** — AI 归纳（200-300 字）

---

## 🔜 后续优化

### 计划中

- [ ] 代码重构（提取公共函数）
- [ ] 单元测试（核心函数覆盖率 80%+）
- [ ] 性能优化（截图并行上传、结果缓存）
- [ ] 支持更多平台（TikTok、Instagram Reels）

---

## 📞 更多文档

- **快速入门**: [README.md](README.md) - 5 分钟上手
- **变更历史**: [CHANGELOG.md](CHANGELOG.md) - 版本演进
- **提示词配置**: [prompt.json](prompt.json) - AI 分析参数

---

**维护人**: Ajay Hao  
**项目地址**: https://github.com/AjayHao/video-summarizer  
**OpenClaw Skill**: 已发布到 clawdhub
