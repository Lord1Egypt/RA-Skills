---
name: scrapt-video
description: "当用户想要克隆、查看、获取、分析、解析抖音/小红书/快手/B站/TikTok/YouTube 链接内容时，必须先用本技能按平台调用对应 scrapt 解析接口（/scrapt/{platform}/parse）拿到视频直链，再自动衔接 describe-video 做字幕+画面深度分析。"
---

# Scrapt Video Skill

用于“社媒链接 -> 视频直链 -> 深度分析”的一体化流程。

适用平台：
- 小红书
- 抖音
- 快手
- B站
- TikTok
- YouTube

## 固定流程

第一步（必须）：按平台路由并调用对应接口拿直链
- 小红书：`POST /scrapt/xiaohongshu/parse`
- 抖音：`POST /scrapt/douyin/parse`
- 快手：`POST /scrapt/kuaishou/parse`
- B站：`POST /scrapt/bilibili/parse`
- TikTok：`POST /scrapt/tiktok/parse`
- YouTube：`POST /scrapt/youtube/parse`

第二步（必须）：从返回中提取 `data.video.url` 作为可访问视频直链

第三步（必须）：调用 `describe-video` 对该直链做深度描述
- `basic` 字幕与分句时间戳
- 画面内容理解（可透传分析 prompt）
- 输出结构化 JSON + 可读 Markdown

## 前置条件

- Python 3
- `requests` 已安装
- `VECTCUT_API_KEY` 已设置
- 若缺失或失效，先调用 `vectcut-login` 技能

## 执行方式

```bash
python <skill-path>/scripts/scrapt_video.py \
  "8.94 复制打开抖音 ... https://v.douyin.com/xxxxxx/ ..." \
  --analysis-prompt "这条视频的结构、钩子、转场和可复刻脚本是什么？"
```

可选参数：
- `--platform`：手动指定平台（`xiaohongshu|douyin|kuaishou|bilibili|tiktok|youtube`）
- `--poll-interval`：describe-video 的 ASR 轮询间隔，默认 `2.0`
- `--timeout`：describe-video 的轮询超时秒数，默认 `600`
- `--json-output`：默认 `scrapt_video_report.json`
- `--md-output`：默认 `scrapt_video_report.md`

## 输出结果

- `scrapt_video_report.json`
  - `meta`：平台、解析接口、文档链接、解析后直链
  - `parse_result`：平台解析接口原始返回
  - `describe_video_report`：深度分析结构化结果
- `scrapt_video_report.md`
  - 平台素材概览
  - describe-video 可读分析内容

## 对应文档

- 小红书：[https://docs.vectcut.com/433862658e0](https://docs.vectcut.com/433862658e0)
- 抖音：[https://docs.vectcut.com/433861888e0](https://docs.vectcut.com/433861888e0)
- 快手：[https://docs.vectcut.com/433861890e0](https://docs.vectcut.com/433861890e0)
- B站：[https://docs.vectcut.com/433861891e0](https://docs.vectcut.com/433861891e0)
- TikTok：[https://docs.vectcut.com/433861892e0](https://docs.vectcut.com/433861892e0)
- YouTube：[https://docs.vectcut.com/433861893e0](https://docs.vectcut.com/433861893e0)
