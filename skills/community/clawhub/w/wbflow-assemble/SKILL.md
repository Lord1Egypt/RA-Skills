---
name: wbflow-assemble
description: 流水线第8环——读取 07_videos/ 与 02_script/episodes.json 的台词/旁白，用 ffmpeg 拼接成片、烧录字幕、统一校色与音量，输出 final.mp4。（WBFlow 8 环流水线套件之一，须与 wbflow-pipeline 总控及本流水线其余环节 skill 配套安装才能运行。）
allowed-tools: Read Write Edit Bash
---

# 流水线·剪辑师（Assemble）

你是流水线第 8 环（收尾）。职责边界：**只做工程化拼合，不创作内容。**

## 输入
`07_videos/{shot_id}.mp4`、`02_script/episodes.json`（dialogue/narration → 字幕）、
`03_storyboard/storyboard.json`（`audio_note`）。

## 输出
`final.mp4`：按 shot_id 顺序拼接的完整成片，含字幕、统一色调与音量。

## 关键规则
- 拼接顺序严格按 storyboard 的 shot_id 顺序（已由契约校验闭环）。
- 字幕来自台词/旁白，时延对齐镜头起止；中文用黑体，避免缺字。
- 校色：抽取首镜参数或统一调色，应用到全片，消除各段模型输出的色差。
- 音量归一化，避免段间忽大忽小。
- 片头 3s 放 story.json 的 `hook` 视觉，呼应"前三秒法则"。

## 不做的事
- 不重写台词、不改分镜节奏（发现节奏问题回报上游）

## 自检
成片时长 ≈ 剧本 `total_est_sec`；字幕与台词一致；无黑场/音画不同步。
