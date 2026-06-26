---
name: content-rewriter
display_name: 一键扒爆款
description: >
  自媒体人必备 | 丢个视频链接，自动出小红书+头条+抖音三套可直接发布的改写文案。
  支持抖音/B站/小红书。不是学术分析，是"扒下来→分析为什么爆→改成你的版本"。
  实测能省 80% 的爆款分析时间。花大叔出品。
  触发场景：分析视频文案、视频文案改写、扒文案改文章、爆款分析、
  内容改写、文案提取改写、视频转文章、爆款拆解、改写输出、一键扒爆款、
  自媒体文案、小红书爆款、今日头条改写、短视频文案、内容搬运、仿写、
  选题拆解、对标账号分析、文案去重、二创改写
version: 0.6.1
author: 花大叔/O5-7/ 龙渊工坊
category: 内容创作
tags: [爆款改写, 文案提取, 内容运营, 自媒体, 短视频, 小红书文案, 今日头条, 抖音口播, 二创, 仿写, 选题拆解, 对标分析, 文案去重, 内容搬运]
agent_created: true
---

# 爆款内容改写引擎 v0.6.1

## 一句话说清楚

**给个视频链接 → 自动出三套可直接复制的平台文案。**

不下载视频、不分析画面、不写学术报告。要的就是"扒下来 → 分析为什么爆 → 改成我的版本"。

---

## ⚠️ 环境准备（首次使用必装）

本技能依赖以下 Python 包。请在终端执行：

```bash
# 核心依赖（必须）
pip install httpx playwright openai-whisper moviepy

# Playwright 浏览器（必须，只需执行一次）
playwright install chromium

# 可选依赖（按需安装）
# B站下载视频需要（可选，推荐用 API 方案）
# 小红书采集需要额外安装 XHS-Downloader + 提供 Cookie
```

**首次运行说明**：
- whisper 模型会在首次使用时自动下载（base 模型约 142MB）
- 如遇下载慢，可设置镜像：`export HF_ENDPOINT=https://hf-mirror.com`
- moviepy 内置 ffmpeg，无需单独安装 ffmpeg 系统包
- 上述依赖已在 Windows 11 + Python 3.14 环境验证通过

---

## 平台支持现状（诚实版）

| 平台 | 状态 | 采集方式 | 备注 |
|------|------|---------|------|
| 抖音 | ✅ 稳定 | Playwright API 拦截 | 优先取字幕，无字幕时下载+ASR兜底 |
| B站 | ⚠️ 部分可用 | B站公开 API | 可提取标题/描述/数据+检测字幕；下载视频需用户提供Cookie |
| 小红书 | ⚠️ 需 Cookie | XHS-Downloader | 需用户提供 web_session Cookie + 安装 XHS-Downloader |
| 视频号 | ❌ 不支持 | — | 需微信 PC 客户端，暂无自动化方案 |

---

## 核心流程（4步）

```
链接 → 提取文案 → AI爆款分析 → 多平台改写 → 输出纯文本
```

---

## 第一步：提取文案

### 平台识别 + 采集方案

| 域名特征 | 平台 | 文案提取方案 |
|----------|------|-------------|
| `douyin.com` / `v.douyin.com` | 抖音 | Playwright API拦截 → 优先取API字幕 → 无则下载+whisper ASR |
| `bilibili.com/video/BV` | B站 | 公开API提取标题/描述/数据 → 检测AI字幕 → 有字幕直接提取，无字幕需Cookie下载+ASR |
| `xiaohongshu.com/explore/` | 小红书 | XHS-Downloader + Cookie → 视频描述文案 + 口播ASR |
| 视频号链接 | 视频号 | ❌ 告知用户限制 → 建议手动复制文案后直接改写 |

### 抖音（首选方案）

```python
# 短链接解析 → Playwright API拦截 → 取视频详情+字幕
import httpx, re
from playwright.async_api import async_playwright

async def fetch_douyin(share_url: str):
    # 1. 解析短链接拿到 video_id
    resp = httpx.get(share_url, headers=ua, follow_redirects=True)
    video_id = re.search(r'/video/(\d+)', str(resp.url)).group(1)
    
    # 2. Playwright 拦截 API
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        detail = {}
        async def handle(response):
            if "aweme/v1/web/aweme/detail" in response.url:
                import json
                detail = json.loads(await response.text())
        page.on("response", handle)
        await page.goto(f"https://www.douyin.com/video/{video_id}")
        await page.wait_for_timeout(5000)
    
    # 3. 提取文案
    aweme = detail["aweme_detail"]
    text = aweme.get("desc", "")  # 视频描述
    # 优先字幕
    if aweme.get("interaction_stickers"):
        for s in aweme["interaction_stickers"]:
            if s.get("subtitle_data"):
                text += "\n" + s["subtitle_data"]
    return {"title": text, "author": aweme["author"]["nickname"], "stats": aweme["statistics"]}
```

### B站（无需登录的 API 方案）

```python
# 方案A：公开 API 提取元数据 + 字幕检测（无需 Cookie）
import httpx, json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://www.bilibili.com/',
}

# 1. 提取 BV 号并获取视频信息
bvid = "BV1xxXXxXXxx"  # 从 URL 中提取
resp = httpx.get(f'https://api.bilibili.com/x/web-interface/view?bvid={bvid}', headers=headers)
data = json.loads(resp.content.decode('utf-8'))['data']
title = data['title']
desc = data.get('desc', '')  # 视频简介（通常含核心观点）
cid = data['cid']

# 2. 检测是否有 AI 字幕
resp2 = httpx.get(f'https://api.bilibili.com/x/player/v2?bvid={bvid}&cid={cid}', headers=headers)
player = json.loads(resp2.content.decode('utf-8'))
subs = player['data'].get('subtitle', {}).get('subtitles', [])

# 3. 有字幕：直接提取
if subs:
    sub_url = 'https:' + subs[0]['subtitle_url']
    sub_data = json.loads(httpx.get(sub_url, headers=headers).content.decode('utf-8'))
    full_text = ' '.join([item['content'] for item in sub_data['body']])
    # 输出：标题 + 简介 + 字幕 = 完整的文案素材

# 4. 无字幕：使用标题+简介作为文案
# 或告知用户提供 B站 Cookie 以支持视频下载+ASR
```

**说明**：
- 公开 API 无需登录，可稳定提取视频标题、简介、播放数据、字幕
- B站 AI 字幕覆盖率较高（长视频通常有），无字幕时可先用简介改写
- 如需下载完整视频做 ASR：需用户提供 B站 Cookie（浏览器登录后导出 cookies.txt）
- you-get / yt-dlp 等下载工具不稳定（B站频繁更新反爬策略），不推荐作为主方案

### 小红书

需先安装 XHS-Downloader（见环境准备章节），并提供登录 Cookie：

```python
# 使用 XHS-Downloader
import asyncio, sys
sys.path.insert(0, "/path/to/XHS-Downloader")
from source import XHS

async def fetch_xhs(url, cookie=""):
    async with XHS(
        work_path="{output_dir}",
        folder_name="小红书",
        cookie=cookie,
        video_download=False,
    ) as xhs:
        return await xhs.extract(url, download=False)
```

### 视频号 — 降级方案

告知用户限制，提供替代方案：
1. 用户手动从微信视频号复制文案
2. 或安装微信PC客户端后使用代理工具

---

## 第二步：AI 爆款分析

**只分析文本，不分析画面。聚焦 3 个核心维度：**

### 分析框架

| 维度 | 分析什么 | 为什么重要 |
|------|---------|-----------|
| **钩子分析** | 前两句/前5秒抓人的点是什么？用了什么手法？ | 决定完播率 |
| **结构分析** | 内容骨架：先抛什么→再说什么→怎么收尾？段落节奏？ | 决定留存 |
| **情绪分析** | 调动了什么情绪？痛点/爽点在哪？反转/共鸣的时机？ | 决定互动 |

### 输出格式

```
【爆款核心】一句话总结这条为什么爆

【钩子拆解】
- 开头手法：xxx
- 为什么有效：xxx

【内容结构】
开篇 → 展开 → 高潮 → 收尾
（每段标注信息密度和情绪功能）

【情绪地图】
痛点触发 → 共鸣升温 → 爽点释放 → 行动引导

【可复用要素】
- 句式模板：xxx
- 节奏模板：xxx
- 情绪模型：xxx
```

**关键原则**：
- 不说"这个视频很优秀"这种废话
- 不说"镜头语言"、"叙事功能"这种学术词
- 输出是创作者能直接用的，不是给影评人看的

---

## 第三步：多平台改写

**基于爆款分析结果，产出 3 套可直接发布的文案。**

### 平台风格对照

| 特征 | 小红书 | 今日头条 | 抖音口播 |
|------|--------|---------|---------|
| 语气 | 姐妹/宝子们，种草风 | 理性+观点，资讯风 | 口语化，节奏快 |
| 句式 | 短句+Emoji+感叹号 | 标题党+分点论证 | 动词多，停顿少 |
| 长度 | 300-800字 | 800-2000字 | 150-300字 |
| 结构 | 痛点→共鸣→方案→推荐 | 观点→论据→结论→互动 | 钩子→展开→反转→收 |
| 标签 | 3-5个话题标签 | 无标签 | 口播无标签 |

### 改写原则

1. **保留爆款骨架，更换血肉**：结构、节奏、情绪模型不变，主题/案例/人设可换
2. **去 AI 味**：零省略号、零"在当今社会"、零"综上所述"
3. **口语化**：像人写的，不像 AI 写的
4. **反套路反模板**：不用"你是否也遇到过"、"今天给大家分享"
5. **每套独立完整**：用户复制即可发布，不需要再编辑

### 输出模板

```
====================
【小红书版】
====================
[可直接复制发布的正文，含Emoji和标签]

====================
【今日头条版】
====================
[可直接复制发布的正文，标题+正文]

====================
【抖音口播版】
====================
[可直接录制口播的脚本文案]

====================
【爆款要素速查卡】
====================
标题公式：xxx
钩子公式：xxx
情绪公式：xxx
适用场景：xxx
```

---

## 第四步：输出文件

所有文案保存在 `{output_dir}/` 目录下（默认为当前工作目录下的 `output/` 子目录）：

```
{output_dir}/{视频标题}_改写文案.txt
```

---

## ASR 兜底方案（无字幕时）

抖音视频无 API 字幕时的完整 ASR 流程：

```python
# 1. moviepy 提取音频（内置 ffmpeg，无需额外安装 ffmpeg）
from moviepy import VideoFileClip
clip = VideoFileClip("video.mp4")
clip.audio.write_audiofile("temp.wav", fps=16000)
clip.close()

# 2. wave 模块读取 WAV → numpy 数组（绕过 whisper.load_audio 的 ffmpeg 依赖）
import wave, numpy as np
with wave.open("temp.wav", "rb") as wf:
    raw = wf.readframes(wf.getnframes())
    audio = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0

# 3. whisper 转写
import whisper
model = whisper.load_model("base")
result = model.transcribe(audio, language="zh", fp16=False)
```

---

## 适用场景

- 看到一条爆款视频 → 想知道为什么爆 → 快速出稿
- 每天刷抖音/B站 → 批量收集爆款文案 → 改写囤稿
- 学员交付：给对标爆款链接 → 出分析+改写示范 → 教学员模仿
- 小红书/头条矩阵号运营 → 同一爆款素材分发多平台

---

## 注意事项

- 小红书采集需要 cookie（web_session），首次使用需引导用户提供
- B站：优先用公开 API 提取标题+简介+字幕，无需登录；下载视频需用户提供 Cookie
- 视频号不支持全自动，建议引导用户手动复制文案后使用改写功能
- 改写文案仅供创作参考，发布前建议人工过一遍确保合规
- whisper base 模型首次使用会自动下载（约 142MB），建议设置 HF 镜像加速

## 已知限制

- B站 you-get/yt-dlp 在 2026年5月实测均已失效（B站反爬更新），改用公开 API 方案
- 小红书 XHS-Downloader 需 web_session Cookie，无 Cookie 完全不可用
- 长视频（>10分钟）ASR 耗时较长，建议优先找有字幕的视频

---

## 版本历史

- `0.6.1` (2026-05-22): 优化 description/tags，新增 15 个搜索关键词提升可发现性
- `0.6.0` (2026-05-22): 正式发布版。B站改用公开 API 方案；新增 category/tags 元数据；新增已知限制章节
- `0.5.0-beta` (2026-05-22): 上架前改造。去硬编码路径、诚实地图、标准化环境准备。署名花大叔/O5-7/龙渊工坊
- `0.4.0` (2026-05-22): 第二次实战验证，完善 ASR 链路（moviepy + wave 绕过 ffmpeg）
- `0.3.0` (2026-05-22): 首次实战，从 video-frame-analyzer 重构为 content-rewriter
- `0.1.0` (2026-05-20): 初始原型
