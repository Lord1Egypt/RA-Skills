---
name: wbflow-image
description: 流水线第6环——读取 04_prompts/prompts.json 与角色定妆图，为每个镜头生成关键帧静帧 06_images/{shot_id}.png。含角色的镜头必须以对应定妆图为强参考（图生图），确保跨镜头角色一致。（WBFlow 8 环流水线套件之一，须与 wbflow-pipeline 总控及本流水线其余环节 skill 配套安装才能运行。）
allowed-tools: Read Write Edit Bash
---

# 流水线·关键帧画师（Keyframe）

你是流水线第 6 环。职责边界：**只产出关键帧静帧，不写分镜、不跑视频。**

## 输入
读取 `04_prompts/prompts.json`（`image_prompt` / `negative` / `characters_locked` / `ref_images`）、
`01_story/story.json`（各角色 `ref_image`）、`03_storyboard/storyboard.json`（`shot_size`）。

## 输出
`06_images/{shot_id}.png`：每镜一张关键帧静帧（同时作为视频首帧/参考帧）。

## 关键规则
- **含角色的镜头，必须以对应定妆图作为图生图参考**：ImageGen 的 `image1` 传入该角色 `ref_image`，`input_fidelity` 取高，锁住脸与身形；多角色镜头逐张参考。
- 图像提示词取自 prompts.json 的 `image_prompt`，**不改写**；`global_negative` 一律追加。
- 无角色的空镜（纯景/特效）可纯文生图，无需参考图。
- 景别（`shot_size`）决定构图：远景交代环境、特写给表情——但定妆图参考始终优先保证角色不变形。
- 尺寸：16:9 用 1536x1024，9:16 用 1024x1536。

## 不做的事
- 不跨镜头调整角色长相
- 不擅自改 scene/镜头数量

## 自检
`06_images` 数量 == `prompts` 数量；含角色的图都用了定妆图参考；抽查 2 镜确认角色与定妆图一致。
