---
name: video-to-mindmap
description: "视频转思维导图 / video to mind map. 用户想把一个长视频（B站网课、YouTube 讲座、播客、抖音长视频）画成思维导图、脑图、markmap 时使用。先读视频拿到「带时间的章节大纲」，再转成 markmap 能直接画的 Markdown：每个分支是一节（标明起止时间），叶子是这一节的要点；短视频没有大纲时用要点画一层。不登录平台、不下载视频。需要 LinkDigest API Key（注册送 10 积分）。"
version: 1.0.0
homepage: https://linkdigest.dev/zh/bilibili-siwei-daotu?ref=skill-video-to-mindmap
metadata: {"openclaw":{"requires":{"anyBins":["python3"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":true,"description":"LinkDigest API Key（ld_live_ 开头），在 https://linkdigest.dev/signin?ref=skill-video-to-mindmap&next=/app/keys 创建，注册送 10 积分"}],"homepage":"https://linkdigest.dev/zh/bilibili-siwei-daotu?ref=skill-video-to-mindmap"}}
required_environment_variables:
  - name: LINKDIGEST_API_KEY
    prompt: "LinkDigest API key (starts with ld_live_)"
    help: "https://linkdigest.dev/signin?ref=skill-video-to-mindmap&next=/app/keys"
    required_for: "reading the video; sign-up gives 10 free credits, no card"
---

# 视频 → 思维导图 (markmap)

Feeding a transcript to a model and asking for a mind map gives hundreds of branches or invented structure. What a mind map needs is the layer in between: a **timed outline** — 5 to 20 sections, each with a start and end time, a title and a few lines. This skill gets that outline from LinkDigest and converts it with a small local script.

## Steps

```bash
export LINKDIGEST_API_KEY=ld_live_...   # https://linkdigest.dev/signin?ref=skill-video-to-mindmap&next=/app/keys

python3 {baseDir}/scripts/linkdigest.py "<video link>" --format json --depth transcript \
  | python3 {baseDir}/scripts/to_markmap.py > map.md
```

Then either paste `map.md` into https://markmap.js.org/repl (draws at once; export SVG/HTML there), or run `npx markmap-cli map.md` for a local HTML file. XMind and most mind-map apps import Markdown too.

`--depth transcript` reads the speech in full with a frame a minute — the cheapest read that still yields an outline. `to_markmap.py --max-minutes 10` marks any section longer than 10 minutes (default 15) so the user knows where to split by hand.

## What the map looks like

Real output of `to_markmap.py` on a live read of 跟李沐学AI《Transformer论文逐段精读》 (first three branches):

```markdown
# Transformer论文逐段精读【论文精读】
- `00:00–00:36` **Transformer模型的地位与影响力**
  - 介绍Transformer是继MLP和CNN后的第四大类模型。
  - 斯坦福综述提议将其称为基础模型，显示其巨大影响力。
- `00:36–01:23` **标题含义与作者贡献说明**
  - 解析标题"Attention is all you need"的双关含义及网络梗。
- `01:23–04:12` **摘要解读：主流序列转录模型现状**
  - 指出主流序列到序列模型依赖循环或卷积神经网络。
```

## Limits to tell the user

- **Outlines exist for videos of 8 minutes and longer read since 2026-11-10.** A shorter video, or one served from an older cached read, has only key points: the map is then one layer, and its first branch says so.
- Section times come from the transcript's own timestamps and are checked in code; titles and lines are written by a model from the transcript, so recognition errors (names, terms) carry through.
- Platforms: Bilibili, YouTube, Douyin, TikTok, Xiaohongshu videos, podcasts with a public page. Private, deleted or members-only videos cannot be read and are not charged.
- The skill does not draw images or produce .xmind files; it produces the Markdown that markmap and mind-map apps draw.

## Cost

Per started minute of video, less for a transcript-first read (an 87-minute lecture is 45 credits). A link already read at that depth is free. The conversion runs locally and costs nothing.

Only the link goes to linkdigest.dev; no platform account or cookie is used. https://linkdigest.dev/privacy · support@linkdigest.dev
