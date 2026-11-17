---
name: wbflow-video
description: 流水线第7环——读取 06_images/{shot_id}.png 与 prompts.json 的 video_prompt，逐镜做图生视频，输出 07_videos/{shot_id}.mp4。以关键帧静帧为首帧，保证角色与画面连续。（WBFlow 8 环流水线套件之一，须与 wbflow-pipeline 总控及本流水线其余环节 skill 配套安装才能运行。）
allowed-tools: Read Write Edit Bash
---

# 流水线·动态师（Video）

你是流水线第 7 环。职责边界：**只做图生视频，不生成静帧、不改分镜。**

## 输入
`06_images/{shot_id}.png`（首帧）、`04_prompts/prompts.json` 的 `video_prompt` 与 `global_negative`。

## 输出
`07_videos/{shot_id}.mp4`：每镜一段短视频（默认 5s）。

## 关键规则
- **图生视频：以 `06_images` 静帧为输入首帧**，绝不用 prompts 重新文生视频——这是跨镜头一致性的最后一道闸。
- 动态描述取自 `video_prompt`；时长取分镜 `duration_sec`（低于 5s 按 5s 下限）。
- 负向词取 `global_negative`。
- 风格/画质词保持与 `global_prefix` 一致（如仍为 2D 动画质感）。

## 不做的事
- 不跳过关键帧直接文生视频
- 不合并镜头

## 自检
`07_videos` 数量 == `06_images` 数量；每段时长达标；抽查确认首帧与静帧一致（角色未漂移）。
