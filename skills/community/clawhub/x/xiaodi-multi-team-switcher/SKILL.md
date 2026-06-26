---
name: xiaodi-multi-team-system
description: 小弟多团队协作系统 - 金融、电商、多媒体、办公四大团队 + 智能切换器
version: "1.0.1"
author: xiaodi
homepage: https://github.com/mx6315909/xiaodi-multi-team-skills
metadata:
  openclaw:
    emoji: 🤖
    requires:
      tools: ["web_search", "web_fetch", "memory_search", "exec", "browser"]
      binaries: ["ffmpeg", "ffprobe", "convert"]
---

# 🤖 小弟多团队协作系统

专业的 AI Agent 团队协作系统，四大功能团队 + 智能切换器，一键切换金融、电商、多媒体、办公场景。

## 📦 团队列表

| 团队 | 图标 | 功能 | 角色数 |
|------|------|------|--------|
| 金融团队 | 📊 | 股票分析、投资决策 | 7 |
| 电商团队 | 🛒 | 选品、运营、定价 | 8 |
| 多媒体团队 | 🎬 | 视频、图片、音频处理 | 7 |
| 办公团队 | 📋 | 日程、邮件、文档 | 4 |

**总计：26 个专业 Agent 角色**

---

## ⚙️ 系统要求

### 必需工具

| 工具 | 用途 | 安装命令 |
|------|------|----------|
| `ffmpeg` | 视频处理 | `apt install ffmpeg` 或 `brew install ffmpeg` |
| `ffprobe` | 视频分析 | 随 ffmpeg 安装 |
| `ImageMagick` | 图片处理 | `apt install imagemagick` 或 `brew install imagemagick` |

### 可选工具

| 工具 | 用途 | 安装命令 |
|------|------|----------|
| `whisper` | 语音识别/字幕生成 | `pip install openai-whisper` |
| `akshare` | A股数据 | `pip install akshare` |

### 权限说明

本技能需要以下工具权限：

- **web_search** - 搜索网络信息
- **web_fetch** - 获取网页内容
- **memory_search** - 搜索记忆
- **exec** - 执行系统命令（ffmpeg、ImageMagick 等）
- **browser** - 浏览器自动化

---

## 🔐 数据源声明

### 金融数据（公开 API）

| 数据源 | 用途 | 认证 |
|--------|------|------|
| 东方财富 | 股票行情、财务数据 | 无需认证 |
| 腾讯财经 | 股票行情 | 无需认证 |
| 新浪财经 | 新闻、舆情 | 无需认证 |

### 电商数据（公开 API）

| 数据源 | 用途 | 认证 |
|--------|------|------|
| 亚马逊 | 商品信息、BSR | 无需认证 |
| TikTok | 商品信息 | 无需认证 |

---

## 🔑 可选 API 配置

AI 视频生成功能需要配置以下环境变量（可选）：

```bash
# 可灵 AI
export KLING_API_KEY=your_key

# Runway Gen-3
export RUNWAY_API_KEY=your_key

# Pika Labs
export PIKA_API_KEY=your_key

# OpenAI (Sora/DALL-E)
export OPENAI_API_KEY=your_key
```

**注意**：这些 API Key 仅用于 AI 视频生成，不配置不影响其他功能。

---

## 🚀 快速开始

### 安装

```bash
clawhub install xiaodi-multi-team-system
```

### 使用示例

```
# 金融场景
分析茅台的投资价值
诊断我的持仓

# 电商场景
帮我选品，类目：美妆护肤
监控竞品价格变化

# 多媒体场景
压缩这个视频 /path/to/video.mp4
提取视频第10秒的帧

# 办公场景
帮我安排明天下午3点的会议
整理这份文档
```

---

## 📋 团队详情

### 📊 金融团队

7 大角色协作：投顾专家、行业研究员、投行专家、市值管理助理、财富专员、商机助理、舆情助理

**数据源**：东方财富、腾讯财经、新浪财经（均为公开 API）

### 🛒 电商团队

8 大角色协作：选品专家、运营专员、定价专员、客服专员、数据分析师、竞品分析师、内容创作者、投放专员

**数据源**：亚马逊、TikTok（公开数据）

### 🎬 多媒体团队

7 大角色协作：视频剪辑师、视频创作师、字幕生成器、图片处理师、AI 绘图师、音频处理师、质量检查员

**依赖**：ffmpeg、ImageMagick、whisper（可选）

### 📋 办公团队

4 大角色协作：日程秘书、邮件秘书、文档秘书、会议秘书

---

## ⚠️ 安全声明

1. **exec 权限**：仅用于调用 ffmpeg、ImageMagick 等媒体处理工具，不会执行任意危险命令
2. **browser 权限**：仅用于获取公开网页数据，不会访问需要认证的私密页面
3. **API Key**：所有 API Key 通过环境变量配置，不会硬编码或存储在代码中
4. **数据安全**：不读取主机敏感文件，不外传用户数据

---

## 📄 License

MIT License

---

## 👤 作者

xiaodi <mxbot-xiaodi@agentmail.to>

---

*GitHub: https://github.com/mx6315909/xiaodi-multi-team-skills*