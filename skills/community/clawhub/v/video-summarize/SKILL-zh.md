---
name: video-summarize
description: 视频总结，触发：1.用户给视频链接（B站/YouTube/抖音/Twitter/TikTok等）、2.总结这个视频
---

# 通用视频总结

智能获取视频文字 → 让大模型总结内容

## 处理流程

```
视频链接 → 检查缓存 → 尝试下载字幕 → 有字幕？ → 直接提取文本 → 总结
                                ↓ 无字幕
                                下载音频 → Whisper转录 → 总结
```

## 特性

- **字幕优先**：优先下载官方/人工字幕，无字幕才用 Whisper 转录
- **多平台支持**：B站、YouTube、抖音、Twitter、TikTok 等 1000+ 平台
- **自动语言检测**：Whisper 自动检测视频语言（中文、英文、日文等）
- **并发安全**：每个视频独立临时文件，支持同时处理多个视频
- **智能缓存**：同一视频再次请求直接返回结果

## 支持平台

基于 yt-dlp，支持 **1000+ 平台**：

| 平台 | 链接格式示例 |
|------|-------------|
| **B站** | `https://www.bilibili.com/video/BVxxx` |
| **YouTube** | `https://www.youtube.com/watch?v=xxx` |
| **抖音** | `https://www.douyin.com/video/xxx` |
| **Twitter/X** | `https://twitter.com/user/status/xxx` |
| **TikTok** | `https://www.tiktok.com/@user/video/xxx` |
| **Instagram** | `https://www.instagram.com/p/xxx` |
| **AcFun** | `https://www.acfun.cn/v/acxxx` |
| **爱奇艺/优酷/腾讯** | 各平台视频链接 |
| **其他** | yt-dlp 支持的任何平台 |

## 依赖安装

脚本会自动检查并安装缺失依赖：
- ffmpeg（音频转换）→ `brew install ffmpeg`
- whisper.cpp（转录）→ `brew install whisper-cpp`
- Python3（完全隔离的 Python虚拟环境）→  `brew install python3`

运行：
```bash
scripts/install_dependency.sh
```

注意：首次使用时安装依赖较多，可能等待时间较长，具体取决于你的网络流畅度。

## 使用方法

```bash
# 处理视频（首次会转录，再次直接返回缓存）
scripts/process.sh "视频链接"
```

流程：
1. 检查缓存（已有则直接返回）
2. 尝试下载字幕（优先中文人工字幕，其次自动字幕）
3. 有字幕 → 提取纯文本；无字幕 → 下载音频 → Whisper 转录
4. 保存到 `summarize_result/{标题}_transcript_raw.txt`

**然后让我总结并保存 md 文件！**

## 输入格式

支持多种格式：
- B站：`https://www.bilibili.com/video/BV1s8UZBZEa8`
- YouTube：`https://www.youtube.com/watch?v=dQw4w9WgXcQ`
- 抖音：`https://www.douyin.com/video/7123456789`
- Twitter：`https://twitter.com/user/status/123456789`
- TikTok：`https://www.tiktok.com/@user/video/123456789`
- 其他 yt-dlp 支持的链接

## 输出

文件名用标题（一眼看出内容），特殊符号自动处理：

```
cache/{标题}/
└── transcript_raw.txt          # 原始转录

summarize_result/
└── {标题}.md                    # 总结
```

**命名处理：**

- 中文标点 `《》【】：？` → `_`
- 英文符号 `/\:*?"<>|` → `_`
- 空格 → `_`
- 连续下划线合并
- 最多 50 字符

## 目录结构

```
video-summarize/
├── cache/                   # 缓存目录
│   └── {标题}/               # 每个视频独立目录
│       ├── transcript_raw.txt  # 原始转录（保留）
│       ├── status.json      # 处理状态（清理）
│       ├── subs/            # 字幕临时目录（清理）
│       ├── audio.m4a        # 音频文件（清理）
│       └── audio.wav        # WAV 格式（清理）
├── summarize_result/        # 总结文件目录
│   └── {标题}.md            # 总结文件
├── whisper-models/
│   └── ggml-base.bin
├── scripts/
│   ├── install_dependency.sh
│   ├── process.sh
│   └── safe_filename.py     # 标题转安全文件名
└── SKILL.md
```

## 字幕支持

| 平台 | 人工字幕 | 自动字幕 |
|------|---------|---------|
| **YouTube** | ✅ 支持 | ✅ 支持 |
| **B站** | ✅ 支持 | ⚠️ 部分支持 |
| **其他** | 视平台而定 | 视平台而定 |

字幕优先级：中文人工字幕 > 英文人工字幕 > 自动字幕

## 注意

- 仅处理公开视频（不支持会员视频、付费视频）
- 字幕质量通常优于 Whisper 转录（优先使用字幕）
- 无字幕时转录质量取决于视频音质和 Whisper base 模型
- 长视频（>30分钟）转录时间较长
- 中文、英文、日文等主流语言转录效果良好
- 需要网络连接下载视频音频/字幕