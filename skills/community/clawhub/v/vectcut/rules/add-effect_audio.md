---
name: add-effect_audio
description: "在关键时间点为口播草稿添加短音效提示（一次即可，不铺满全片），用于开头抓注意力、重点关键词强化、画中画切入提示。用户提到“加提示音/重点音效/开头叮一下/关键词音效/画中画提示音”时必须使用本技能。"
---

# Add Effect Audio Skill

用于在关键位置添加“短提示音效”，强调当前讲述内容或画面重点。和背景音乐不同，本技能是单次点缀，不做全片铺满。

官方接口文档：
- get_duration: https://docs.vectcut.com/328289318e0
- add_audio: https://docs.vectcut.com/321196190e0

## 何时使用

- 用户要求加“提示音/重点音效/叮一下”
- 开头需要一个抓注意力的提示音
- 中间出现重点关键词，需要声音强调
- 画中画切入、重点镜头出现时，需要短音效提示

## 鉴权前置（必须）

- 检查 `VECTCUT_API_KEY` 是否可用
- 缺失、为空或疑似失效时，先调用 `vectcut-login`

## 音效来源

- 默认读取技能内置白名单：`<skill-path>/references/effect_audios.json`
- 若用户提供 `effect_audio_url`，优先使用用户链接
- 若未指定：
  - 默认取白名单第一条
  - 可用 `effect_audio_index` 按序号选
  - `random_effect_audio=true` 时随机选

## 执行策略（与 BGM 区分）

- 本技能默认“添加一次”即可，不循环铺满
- 默认开头触发：`target_start=0`
- 重点位由用户指定时间点：`target_start=<秒>`
- 音效时长通过 `get_duration` 获取，默认整段添加；需要更短可传 `clip_duration`

## 执行方式

准备请求 JSON，例如：

```json
{
  "draft_id": "dfd_xxx",
  "target_start": 0.0,
  "effect_audio_index": 0,
  "track_name": "audio_effect",
  "volume": 0.0
}
```

执行脚本：

```bash
python <skill-path>/scripts/add_effect_audio.py \
  "/tmp/add_effect_audio_payload.json" \
  --output "./add_effect_audio_result.json"
```

## 输入说明

- 必填：
  - `draft_id`
- 常用可选：
  - `target_start`：音效放置时间点（秒），默认 `0.0`
  - `effect_audio_url`：直接指定音效链接
  - `effect_audio_index`：白名单索引
  - `random_effect_audio`：是否随机选音效
  - `clip_duration`：截取时长（秒），默认音效全长
  - `track_name`：默认 `audio_effect`
  - `volume`：单位 dB，默认 `0.0`
  - `speed`：默认 `1.0`
  - `effect_audio_list_path`：自定义音效白名单路径

## 输出结果

默认输出 `add_effect_audio_result.json`，核心字段：
- `meta.selected_effect_audio_url`
- `meta.source_duration_seconds`
- `meta.clip_duration_seconds`
- `meta.target_start_seconds`
- `result.draft_id`
- `result.draft_url`
- `result.material_id`

## 失败处理建议

- `VECTCUT_API_KEY` 缺失：先调用 `vectcut-login`
- `draft_id` 无效：先确认草稿可访问
- 音效白名单为空：检查 `references/effect_audios.json` 或自定义列表
- `get_duration` 失败：检查音效链接可访问性
- `add_audio` 失败：检查 `target_start/volume/speed` 参数
