---
name: research-paper-portal
description: 为研究人员创建个性化学术论文导航网站。根据用户的研究领域，自动收集最新论文、生成AI背景图、发布到网站。触发词：创建论文导航网站、学术门户、研究论文网站、论文聚合站、论文导航页。
---

# Research Paper Portal

为研究人员快速构建个性化的学术论文导航网站。

## 功能特性

- **论文自动收集**：从 OpenAlex、arXiv、RSS 等源获取最新论文
- **AI 背景图生成**：使用 Flux2 为每篇论文生成独特背景
- **渐进式图片加载**：WebP 格式，预览图→高清图过渡
- **论文数据管理**：队列机制、定时发布
- **响应式设计**：支持桌面和移动端

## 快速开始

### 第一步：了解用户需求

在开始部署前，询问用户以下信息：

```
请提供以下配置信息：

1. 研究领域（关键词）
   - 例如：thermoelectric, heat pipe, geothermal
   - 或：machine learning, computer vision
   - 或：cancer research, immunotherapy

2. 网站名称
   - 例如：Thermoelectric.Tech

3. 大语言模型（LLM）资源
   - 推荐：Gemini CLI（免费）或 Claude API
   - 用途：论文摘要翻译、标题生成

4. 绘图模型资源
   - 推荐：ComfyUI + Flux2
   - 服务器地址：例如 http://192.168.1.100:8188

5. Web 服务器
   - 推荐：Caddy（自动 HTTPS）
   - 或：Nginx、Apache
```

### 第二步：部署网站

1. 复制网站模板到用户的服务器目录
2. 配置 Web 服务器
3. 设置定时任务

### 第三步：配置工作流

创建配置文件 `config.json`：

```json
{
  "siteName": "YourResearch.Tech",
  "keywords": ["keyword1", "keyword2"],
  "paperSources": {
    "openalex": true,
    "arxiv": true,
    "rss": []
  },
  "llm": {
    "provider": "gemini",
    "command": "gemini -p"
  },
  "imageGeneration": {
    "comfyui_url": "http://YOUR_SERVER:8188",
    "workflow": "flux2_text_to_image"
  },
  "publishSchedule": {
    "updatePapers": "05:00",
    "publishSite": "08:00"
  }
}
```

## 工作流程

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  论文收集脚本    │ ──▶ │   发布队列       │ ──▶ │   定时发布      │
│ (每日凌晨运行)  │     │ (待发布论文+图片) │     │  (每日早晨)     │
└─────────────────┘     └──────────────────┘     └─────────────────┘
        │                        │
        ▼                        ▼
  ┌───────────┐            ┌───────────┐
  │ LLM 翻译  │            │ AI 生成图  │
  │ 标题+摘要 │            │ 背景图片   │
  └───────────┘            └───────────┘
```

## 资源说明

### assets/
- `index.html` - 网站主页面模板
- `admin.html` - 管理后台模板

### scripts/
- `update-papers.py` - 论文收集脚本
- `generate-bg.py` - AI 背景图生成
- `convert-images.py` - 图片格式转换
- `daily-publish.py` - 每日发布脚本

### references/
- `CONFIG.md` - 详细配置说明
- `API.md` - OpenAlex/arXiv API 使用说明
- `COMFYUI.md` - ComfyUI Flux2 工作流说明

## 定时任务配置

使用 OpenClaw cron 或系统 crontab：

```bash
# OpenClaw cron
openclaw cron add --name "论文更新" --schedule "0 5 * * *" --script "update-papers.py"
openclaw cron add --name "网站发布" --schedule "0 8 * * *" --script "daily-publish.py"

# 或系统 crontab
0 5 * * * python /path/to/update-papers.py
0 8 * * * python /path/to/daily-publish.py
```

## 注意事项

1. **API 限制**：OpenAlex 免费无限制，arXiv 建议每 3 秒一次请求
2. **图片存储**：建议每张预览图 <50KB，高清图 <200KB
3. **论文数量**：建议每日发布 3-5 篇，保证质量
4. **备份**：定期备份 `paper-index.json` 和 `pending-papers.json`

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 论文数据为空 | 检查关键词拼写，确认 API 可访问 |
| 图片生成失败 | 检查 ComfyUI 服务状态，确认模型已加载 |
| 网站无法访问 | 检查 Web 服务器配置，确认端口开放 |
| 中文显示乱码 | 确认文件 UTF-8 编码，检查 Content-Type |
