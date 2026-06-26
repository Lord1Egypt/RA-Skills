# xhs-publish 使用说明

## 简介

xhs-publish 是一个小红书一键发布助手，帮助用户快速生成并发布小红书笔记。

## 功能特点

- ✅ 支持三种笔记类型：纯封面图、 知识卡片、 视频笔记
- ✅ 自动生成标题（5个）+ 正文 + 封面/知识卡片/视频
- ✅ 支持 MCP 服务（MD2Card）
- ✅ 自动发布到小红书

## 快速开始

### 1. 基本使用

```
用户：帮我发个小红书，关于 OpenClaw

AI：请选择笔记类型：
1. 📷 纯封面图 — AI 生成单张封面图 + 正文
2. 🖼️ 知识卡片 — 生成精美知识卡片 + 正文
3. 🎬 视频笔记 — AI 生成视频 + 正文

用户：2

AI：请选择封面生成方式：
1. 🎨 AI 模型生图
2. 📝 MD2Card 一句话封面

用户：2

AI：[生成封面 + 正文]

📝 笔记内容已生成！

**标题**（默认第一个）：
1. OpenClaw 是什么？3分钟带你搞懂✨
2. 谁懂啊🤔这个框架让我效率翻倍！
...

**正文**：
[正文内容]

**封面**：[图片]

是否满意？
1. 满意，直接发布
2. 换个标题
3. 重新生成正文
4. 重新生成封面
5. 全部重新生成

用户：1

AI：[自动发布到小红书]
```

### 2. 知识卡片生成

```
用户：帮我发个小红书，关于 OpenClaw，选择知识卡片

AI：[生成封面 + 知识卡片内容]

🖼️ 封面预览
[封面图片]

🖼️ 知识卡片预览
[知识卡片图片 1]
[知识卡片图片 2]
...

是否满意？

用户：满意

AI：[自动发布到小红书]
```

### 3. 视频笔记生成

```
用户：帮我发个小红书
关于 OpenClaw
选择视频笔记

AI：[生成分镜脚本 → 生成视频片段 → 合并视频 → 添加字幕]

🎬 视频预览
[视频]

是否满意？

用户：满意

AI：[自动发布到小红书]
```

## 配置要求

### 1. AI 生图 API

```bash
# 方式1：豆包（Doubao）API
export DOUBAO_API_KEY="your-api-key"

# 方式2：腾讯混元 API
export HUNYUAN_SECRET_ID="your-secret-id"
export HUNYUAN_SECRET_KEY="your-secret-key"
```

### 2. MD2Card MCP（可选）

```bash
# 安装 MCP 服务
npm install -g md2card-mcp-server@latest

# 申请 API 密钥
https://md2card.cn/zh/login

# 配置环境变量
export MD2CARD_API_KEY="your-api-key"
```

### 3. 小红书 MCP

```bash
# 安装依赖
sudo apt install -y xvfb imagemagick zbar-tools xdotool fonts-noto-cjk

# 下载 MCP
mkdir -p ~/xiaohongshu-mcp && cd ~/xiaohongshu-mcp
wget https://github.com/xpzouying/xiaohongshu-mcp/releases/latest/download/xiaohongshu-mcp-linux-amd64.tar.gz
tar xzf xiaohongshu-mcp-linux-amd64.tar.gz
chmod +x xiaohongshu-*

# 启动服务
Xvfb :99 -screen 0 1920x1080x24 &
export ROD_DEFAULT_TIMEOUT=10m
DISPLAY=:99 nohup ./xiaohongshu-mcp-linux-amd64 -port :18060 > mcp.log 2>&1 &
```

## 常见问题

### Q1：发布失败怎么办？

**A**：系统会自动重试 1 次。如果仍然失败，会自动获取登录二维码，让你扫码重新登录。

### Q2：MD2Card MCP 未安装怎么办？

**A**：系统会自动使用浏览器自动化方式生成（较慢但可用）。

### Q3：知识卡片需要手动切割吗？

**A**：不需要！系统会自动切割为多张 1080x1440 图片。

### Q4：字数要求是多少？

**A**：
- 纯封面图：正文 600-800 字
- 知识卡片：正文 600-800 字，知识卡片内容 2000-3000 字
- 视频笔记：正文 200-300 字

## 技术支持

- GitHub: https://github.com/openclaw/xhs-publish
- 文档: {baseDir}/skills/xhs-publish/SKILL.md
