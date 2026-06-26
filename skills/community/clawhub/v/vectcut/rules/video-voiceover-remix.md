---
name: video-voiceover-remix
description: 给一段或多段视频做“随机重排 + 网感解说配音 + 字幕 + BGM + 开头提示音”的自动成片能力。用户提到“视频配音”“多段视频随机组合并配旁白”“B-roll混剪后自动解说”“批量视频做网感讲解”时，在 vectcut-skill 内必须优先编排本链路。
---

# Video Voiceover Remix（聚合子链路）

用于把一个或多个视频素材自动整理成“静音 B-roll + 画外音解说 + 模板字幕 + 背景音乐 + 开头提示音”的完整草稿。

## 固定执行链路（七步）

1. `describe-video`：先分析所有上传视频（素材盘点与内容理解）。
2. `add_video`：随机重排片段写入 B-roll，且每段 `volume=-100`（静音）。
3. 基于 `describe-video` 的分析结果生成网感解说文案：有钩子、有话题性，并按草稿时长等比控制字数（每秒约 5 字）。
4. `speech-synthesis` + `add_audio`：生成配音并写回草稿，配音 `volume=20`，默认音色 `voice_id=gv_8195cd8b03f74658a9d92c9b2a9e9cba`。
5. `llm-asr` + `add-subtitle-template`：先对第 4 步配音做 `nlp` 字幕识别，再上模板字幕。
6. `add-bgm`：补背景音乐（铺满全片）。
7. `add-effect_audio`：在开头添加关键点提示音（一次）。

## 前置约束

- 调任何 VectCut 接口前先检查 `VECTCUT_API_KEY`。
- 若 token 缺失或失效，先走 `vectcut-login`。
- 输入素材需为公网 URL；本地素材先走 `sts-upload`。

## 第 2 步：随机重排并静音写入 B-roll

优先使用本技能内置脚本：

```bash
python <skill-path>/scripts/remix_and_add_videos.py \
  "/tmp/remix_payload.json" \
  --output "/tmp/remix_result.json"
```

执行规则：

- 必须随机顺序组合片段（不是固定原顺序）。
- 每个 `add_video` 请求都强制 `volume=-100`。
- 通过 `start/end/target_start` 对齐时间轴，不允许重叠覆盖。
- 官方接口文档：`add_video` https://docs.vectcut.com/321243745e0

## 第 3 步：文案长度

- 先结合第 1 步 `describe-video` 的素材分析结果，提炼可讲述的话题、画面亮点与节奏线索。
- 再用 `query-draft` 获取草稿时长 `draft_duration_seconds`。
- 推荐字数：`round(draft_duration_seconds * 5)`。
- 结构建议：开头钩子 + 中段节奏叙事 + 结尾互动话题。

## 第 4 步：配音规则

- `speech-synthesis` 默认使用：`voice_id=gv_8195cd8b03f74658a9d92c9b2a9e9cba`。
- 若用户想换音色，提示去 VectCut 官网查看可用音色后再指定 `voice_id`。
- `add_audio` 写回时固定：`target_start=0`、`volume=20`、`track_name=audio_voiceover`（推荐）。

## 字幕与收口

- 字幕上屏必须使用 `llm-asr --effect-mode nlp`，禁止 `basic` 上屏。
- 再调用 `add-subtitle-template` 上屏。
- 最后调用 `add-bgm` 铺满全片，并用 `add-effect_audio` 在 `target_start=0` 添加一次提示音。

## 输出要求

- 返回：`draft_id`、`draft_url`。
- 返回链路摘要：重排片段、配音文案、字幕模板、BGM 与提示音结果。
- 任一步失败时返回失败步骤、原始错误、建议修复动作，不得伪造成功。
