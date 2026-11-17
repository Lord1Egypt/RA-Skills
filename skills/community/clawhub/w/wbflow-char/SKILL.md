---
name: wbflow-char
description: 流水线第5环——读取 01_story/story.json 的角色设定，为每个角色生成"定妆参考图"（正面全身、中性背景、锁定配色与 identity_lock 强符号），并回写 ref_image 路径到 story.json。这是解决跨镜头角色一致性的关键一环。（WBFlow 8 环流水线套件之一，须与 wbflow-pipeline 总控及本流水线其余环节 skill 配套安装才能运行。）
allowed-tools: Read Write Edit Bash
---

# 流水线·定妆师（Char Sheet）

你是流水线第 5 环。职责边界：**只产出角色参考图与映射表，不动剧情/分镜/提示词。**

## 为什么必须存在（2026-10-21 实测教训）
先前版本只靠文字 `appearance_lock` 注入提示词，3 条独立文生视频跑出来后，铁拐李在远景（SH001）与特写（SH006）里"不像同一个人"。
**结论：文字锁定是弱约束**——能保证主色与轮廓，锁不住脸与身形。
**定则：文字锁主色与强符号，图片锁脸与身形。** 本环节在生图/生视频之前，先为每个角色定一张"标准像"，后续所有镜头以它为参考（图生图 / 图生视频），一致性提升一个量级。这是整条流水线从"能跑"变成"能出片"的分水岭。

## 输入
读取 `01_story/story.json`（只读），遍历 `characters[]`。

## 输出
1. `05_chars/{id}.png`：每位角色一张**正面全身标准像**
   - 中性/透明背景，便于当作参考图抠出主体
   - 严格还原 `appearance_lock` 全部视觉要素（发型/服饰/配色/标志性道具）
   - 姿态端正、无动态、无遮挡、正面平视——这是"参考基准"，不是"画面"
   - 画风与 `style_guide.art_style` 一致
2. `05_chars/README.md`：id → 图片路径 → appearance_lock 对照表，供其它环节引用
3. **回写 `01_story/story.json`**：给每个 character 增加字段 `"ref_image": "05_chars/{id}.png"`

## 关键规则
- 一张图只画一个角色，绝不与其它角色同框（避免参考图互相污染）。
- 图像提示词结构：`[style_guide.art_style] + [appearance_lock 原样] + full-body front view, neutral background, flat color, no action, front-facing`。
- 配色必须落在 `style_guide.palette` 内，禁止引入新色。
- 若某角色 `appearance_lock` 不足以单独成图（如缺"全身/朝向"信息），先回报上游补全，**不臆造**。
- 生成后肉眼核对：脸型/服饰/道具是否与设定一致；不一致则重生成，不将就。

## 不做的事
- 不画分镜画面、不画动态姿势
- 不修改人设

## 自检
每位角色都有 `05_chars/{id}.png` 且 story.json 已回写 `ref_image`；对照表与设定一致。
