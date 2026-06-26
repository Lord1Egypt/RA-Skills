---
name: youtube-daily-digest
description: |
  每日 YouTube AI/产品/科技播客更新摘要。零配置：装了 OpenClaw + 飞书 bot 就能直接用。
  自动抓取 13 个精选频道最新视频字幕，AI 生成中文梗概，飞书卡片推送。
  触发词：YouTube 每日推送、播客摘要、daily digest、订阅更新。
---

# YouTube Daily Digest

每天自动推送 AI/产品/科技领域 13 个精选 YouTube 频道的更新摘要。

## 零配置使用

```bash
pip3 install youtube-transcript-api openai --break-system-packages
cd path/to/youtube-daily-digest
FEISHU_USER_OPEN_ID=用户的open_id python3 scripts/digest.py
```

脚本自动从 `~/.openclaw/openclaw.json` 读取飞书 appId/appSecret 和 Gateway token。

## 定时推送

```bash
openclaw cron add \
  --name "youtube-daily-digest" \
  --cron "0 11 * * *" \
  --tz "America/New_York" \
  --description "每日 YouTube 播客摘要推送" \
  --message "cd ~/.openclaw/workspace/skills/youtube-daily-digest && FEISHU_USER_OPEN_ID=用户open_id python3 scripts/digest.py" \
  --session isolated --timeout 600000 --announce --channel feishu
```

## 用户要添加/删除频道时

直接编辑 `scripts/digest.py` 顶部的 `CHANNELS` 列表。channel_id 获取方式见 `references/setup.md`。

## 踩坑指南（重要，必读）

详见 `references/setup.md`，包含所有已验证的坑和解决方案。

## 内置频道

Lex Fridman · Lenny's Podcast · a16z speedrun · Latent Space · AI Engineer · Aakash Gupta · App Breakdown · WhynotTV · Ben Erez · Brock Mesarich · David Ondrej · Paul J Lipsky · Ali H. Salem

## 技术架构

```
YouTube 原生 Atom RSS → 获取最新视频列表（不需要 Docker/RSSHub）
                ↓
youtube-transcript-api → 免费获取英文字幕（yt-dlp 备用）
                ↓
OpenClaw Gateway → 调用 Claude 生成中文标题翻译 + 梗概
                ↓
飞书互动卡片推送 → 蓝色主题，含序号/频道名/标题/中文翻译/梗概
```
