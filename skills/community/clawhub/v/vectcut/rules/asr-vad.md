---
name: asr-vad
description: "对 ASR 识别字幕做去气口/去错句/去重并重建时间轴字幕。用户在 llm-asr 之后提到“去气口”“口播精剪”“删除嗯啊呃”“保留有效句子”时必须使用本技能；若后续要上屏，需输出按片段裁剪的 add_video(start/end/target_start) 工作流，并基于字幕给出 human-pip 穿插建议。"
---

# ASR VAD Skill

本技能是“两阶段流程”：
- 第一步（语义标记）：由本技能完成 `keep/drop` 标注（去气口、去错句、去重）
- 第二步（物理裁剪）：由 `scripts/asr_vad.py` 执行删除与时间轴重建
- 输出新的连续时间轴字幕（不是原始时间）
- 输出 `add_video` 片段拼接工作流（必须带 `start/end/target_start`）

## 鉴权前置（必须）

- 本技能涉及 VectCut 工作流调用时，先检查 `VECTCUT_API_KEY`
- 若缺失或失效，必须先调用 `vectcut-login` 完成登录与 token 校验

## 何时使用

- 用户说“去气口”“把嗯啊呃删掉”“口播精剪”“去口误重说”
- 用户已完成 `llm-asr`，要继续清洗字幕并生成可剪辑分段
- 用户希望字幕和素材片段严格对齐并连续

## 输入优先级

优先接收 `llm-asr` 输出 JSON（通常含 `full_text`、`raw_result.segments`、`editable_subtitles`）。

第一步标记完成后，传给脚本的输入应为“已标注结果”，至少包含：
- `sentence`（或 `text`）
- `start_time`、`end_time`
- `action`（`keep/drop`）
- `drop_reason`（可选）

兼容说明（自动标准化）：
- 若输入是 `llm-asr` 直接产物的 `editable_subtitles[start_ms/end_ms/text]`，脚本会自动映射为 `sentence/start_time/end_time/action`
- 自动映射场景下，`action` 默认填 `keep`，并在输出 `meta.label_source` 标记为 `auto_default`

脚本入口：

```bash
python <skill-path>/scripts/asr_vad.py \
  --input "./subtitle_editable.json" \
  --output "./subtitle_vad_editable.json" \
  --workflow-output "./asr_vad_clip_workflow.json"
```

可选参数：
- `--video-url`：当输入 JSON 中没有 `source_url` 时显式传入
- `--draft-id`：如需基于已有草稿继续编辑

## 去气口规则（按两阶段）

第一阶段：标记 `keep/drop`（技能职责）
- 依据语义与上下文标记 `action`
- `drop_reason` 允许值：`filler | mistake | repeat | restart | pause | other`
- 规则基线：
  - 去气口：删除“嗯/啊/呃”等无实义语气片段
  - 去错句与重说：删除“说错了/重说/刚才不算/重来”等撤回片段
  - 去重复：相邻语义重复，保留更完整者
  - 语义完整：不保留仅功能词的碎片
  - 保守策略：不确定时保留

第二阶段：按标记重建片段（脚本职责，仅消费已标注结果）
- 仅对 `keep` 片段生成新字幕
- 时间边界必须来自词级时间戳：
  - `start_time` = 首个有效词 `start_time`
  - `end_time` = 末个有效词 `end_time`
  - 必须满足 `start_time < end_time`
- 单条文本建议不超过 12 个汉字，超长按自然语义继续拆分
- 去除标点后再输出 `sentence/text`

## 输出产物

脚本默认输出三个层面：
- `vad_decisions`：已标注的 `keep/drop` 决策（由第一步输入）
- `editable_subtitles`：去气口后、连续新时间轴字幕（可直接上屏）
- `workflow_json`：按保留片段拼接视频的工作流

失败策略（必须）：
- 若无法解析出任何有效 `decisions`，脚本直接报错并退出，不允许静默返回空工作流

`workflow_json` 里 `add_video` 必须使用：
- `start`：原素材截取开始时间（秒）
- `end`：原素材截取结束时间（秒）
- `target_start`：目标轨道开始时间（秒）
- `track_name`：目标轨道（默认建议 `video_main`）

`add_video` 参数细节与更多示例，请优先参考官方接口文档：https://docs.vectcut.com/321243745e0

## 画中画增强建议

- 不在 `asr_vad.py` 里做硬编码关键词匹配
- 基于 `editable_subtitles`，在技能执行步骤中按上下文语义人工/智能判断是否需要穿插 `human-pip`
- 建议输出一个独立的建议清单（可作为后续执行输入），每条建议至少包含：
  - `target_start`
  - `duration_sec`
  - `recommended_template`
  - `preferred_background_type`
- 推荐链路：
  1. 根据建议语义决定背景类型（图或视频）
  2. 背景不足时：
     - 图：调用 `generate-ai-image`
     - 视频：调用 `generate-ai-video`
  3. 调用 `human-pip` 生成抠像画中画并插入草稿

## 上屏执行与对齐检查（必须）

1. 若用户要生成草稿，调用 `execute_workflow` 执行 `workflow_json`
2. 执行后调用 `query-draft` 检查：
   - 字幕是否与视频片段对齐
   - 片段是否连续（无异常重叠/断档）
   - `human-pip` 片段是否按建议时点正确穿插
3. 若不连续，优先修正 `target_start` 累积逻辑后重试
4. 需要更细粒度控制 `add_video` 参数时，参考官方接口文档：https://docs.vectcut.com/321243745e0

## 返回给用户的信息

- 去除统计：总片段、保留数、删除数、删除原因分布
- 输出文件路径：新字幕 JSON、工作流 JSON
- 若已执行工作流：返回 `draft_id` 和 `draft_url`
