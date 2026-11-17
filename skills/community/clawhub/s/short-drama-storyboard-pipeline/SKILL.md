---
name: short-drama-storyboard-pipeline
description: >
  短剧/漫剧分镜提示词流水线：把剧本片段或分镜表批量转成首帧图提示词与图生视频提示词
  （I2V 首帧驱动 / FL2V 首尾帧），适配即梦、可灵、海螺 H3、Seedance、Vidu、Runway
  六类模型方言，内置角色一致性锚点、竖屏 9:16 镜头语言与 CSV/JSON 批量导出。
  Use when the user wants to batch-generate storyboard image prompts or image-to-video
  prompts for AI short drama / comic drama (短剧、漫剧、AI 短剧、分镜、图生视频、首尾帧、
  角色一致性), or needs model-specific prompt dialects (Jimeng, Kling, Hailuo H3,
  Seedance, Vidu, Runway). Not for single standalone clips, video editing, or full
  film assembly.
version: 1.0.2
compatibility: Portable to any agent that reads local files (OpenClaw / LobsterAI / Claude Code / Codex CLI). 零外部 API 依赖；scripts/export_prompts.py 可选增强，仅需 Python 3.8+ 标准库。
metadata:
  openclaw:
    emoji: 🎬
---

# 短剧分镜提示词流水线（Short Drama Storyboard Prompt Pipeline）

一条从「剧本/分镜表」到「可粘贴进生成工具的提示词包」的批量流水线。核心价值：
一次处理整集 20-50 个镜头；角色锚点逐字锁定；按目标模型方言输出，不混用。

## 何时使用

- 用户给了短剧/漫剧剧本、小说片段或分镜表，要批量生成「生图提示词」和「图生视频提示词」
- 用户抱怨跨镜头角色脸崩，需要一致性锚点方案
- 用户指定目标工具（即梦 / 可灵 / 海螺 / Seedance / Vidu / Runway）要对应方言的提示词
- 用户要把分镜成果导出成 CSV/JSON 交给批量生产工具

**不适用**：单条独立视频、剪辑合成、完整成片流水线（那是成片工作流的职责）。

## 流水线总览

```
剧本片段/分镜表
   │  Step 1 分镜表标准化（六列 + 一致性字段）
   ▼
标准化分镜表（Markdown 表格或 CSV）
   │  Step 2 角色一致性锚点（逐字锁定串）
   ▼
锚点表 characters
   │  Step 3 提示词批量生成（首帧图 + I2V/FL2V，按模型方言）
   ▼
逐镜提示词（S01.image / S01.video.i2v / S01.video.fl2v）
   │  Step 4 批量导出与校验（scripts/export_prompts.py）
   ▼
提示词包：逐镜 TXT + manifest.csv + manifest.json
```

## Step 1：分镜表标准化

读取 `references/storyboard-spec.md`，把用户的剧本/粗分镜整理成标准列：

```
shot_id | scene | shot_size | camera_move | duration_s | characters |
action_visual | dialogue_vo | sfx_music | frame_mode | negative_extra
```

规则：竖屏短剧单镜 4-15 秒（超了拆镜）；`frame_mode` 三选一 `i2v | fl2v | t2v`；
镜号连续；`characters` 必须能对上锚点表。用户的输入只有梗概时，按
`references/shot-vocabulary.md` 的短剧镜头节奏补全（黄金 3 秒开场、每 15-30 秒
一个钩子、集末悬念定格）。

## Step 2：角色一致性锚点

读取 `references/consistency-anchor.md`，为每个出场角色生成一条**逐字锁定串**：

```
<ANCHOR 沈青梧> 26岁中国女性，齐腰黑直发中分，左眼角小泪痣，瓜子脸杏眼，
身高165cm纤细；本集服装：月白色改良旗袍立领盘扣，银色小圆耳环。
</ANCHOR>
```

铁律：同一角色在所有镜头的锚点串**逐字相同**（服装变化走分层字段，不改基础锚点）。
先出锚点表让用户确认，再进 Step 3——锚点错了后面全部返工。

## Step 3：提示词批量生成

读取 `references/model-dialects.md` 确认目标模型方言，逐镜产出三件套：

1. `S{nn}.image.txt` — 首帧图提示词：`风格前缀 + 锚点串 + action_visual 画面化
   + 景别/机位 + 竖屏构图 + 负面提示词`
2. `S{nn}.video.i2v.txt` — 首帧驱动视频提示词：从首帧出发的运动描述
   （主体动作 + camera_move + 时长匹配）
3. `S{nn}.video.fl2v.txt` — 首尾帧提示词（仅 `frame_mode=fl2v` 的镜头）：描述
   首帧→尾帧的连续路径，尾帧取下一镜首帧或本镜钩子定格

方言要点速记（细节见 model-dialects.md）：

1. 海螺 H3：英文输出，`integrated_multimodal_description → overall_soundscape
   → non_diegetic_music` 三段结构，4-15s，参考图用 `<Picture 1>` 标签
2. 即梦/可灵/Seedance：中文可直接用，首尾帧模式优先，运镜词放句首
3. Vidu：用角色参考图（主体参考）模式保一致性
4. Runway：英文，句子短，首尾帧用 keyframe 上传表达
5. 模型参数（时长档位、分辨率）随版本变化快——生成前提醒用户以当期官方文档为准

## Step 4：批量导出与校验（可选增强，需 Python 3.8+）

```bash
python3 scripts/export_prompts.py --input 分镜表.csv \
  --outdir out/EP01 --mode both --model hailuo
```

- `--mode scaffold`：按分镜表生成逐镜提示词模板文件（占位符待填）
- `--mode manifest`：输出 manifest.csv / manifest.json 批量清单
- `--mode both`：两者都要
- `--model hailuo|jimeng|kling|seedance|vidu|runway|generic`：按模型校验时长档位
- `--check`：只校验不生成（列完整性、时长范围、锚点缺失、frame_mode 合法性）

## 输出约定

```
out/EP01/
  S01.image.txt  S01.video.i2v.txt  (S01.video.fl2v.txt)
  S02.image.txt  S02.video.i2v.txt
  ...
  manifest.csv   manifest.json
```

用户拿到后按 manifest 逐镜粘贴到目标工具，或导入批量生产工具。

## 硬规则

1. 锚点逐字锁定：任何镜头不得改写角色外观描述
2. 时长匹配：提示词描述的运动量必须与 duration_s 匹配，不写跨镜时间
3. 方言不混用：一次会话锁定一个目标模型；要换模型，全量重导出
4. 对白/字幕文字保留原文语言，不翻译进提示词
5. 版权护栏：用户素材须为自有版权/已授权/公版内容，发现疑似侵权素材先提醒

## 进阶版（可选）

本技能永久免费、持续更新。若还需要**成片合成脚本（拼接+配音+字幕+BGM）、漫剧宫格模板库（9/16/25格）、一键上手脚本与视频教程**，可另购 Pro 版（一次买断，12 个月免费更新）：

- 爱发电：https://afdian.com/item/2e33aad6ad3111f195dc52540025c377

说明：Pro 版为可选增值内容，不影响本免费版的任何功能。
