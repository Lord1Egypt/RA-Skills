***

name: llm-asr
description: "使用 VectCut 的异步 LLM ASR 接口提交字幕识别任务并轮询结果（支持 basic|nlp 与 asr/sta 两种模式）。当用户需要音视频转写、提取时间轴字幕、获取分段 segments、按文案对齐识别时务必使用本技能；只要结果将用于字幕制作/上屏，必须使用 nlp，禁止用 basic 结果直接做字幕。若输入是本地文件，先用 sts-upload 获取公网 URL 再识别。"
------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# LLM ASR (Async) Skill

用于把音视频链接提交为异步字幕任务，并在任务完成后产出可编辑 JSON。

文档引用（保持与原请求一致，优先据此获取最新接口信息）：

- <https://docs.vectcut.com/442852943e0>
- <https://docs.vectcut.com/442852944e0>

本技能只做“识别与结构化输出”，不做“自动写回草稿”：

- 输出为文本与时间轴结构
- 不会自动把字幕写入草稿
- 若需要上屏，请把输出 JSON 用于后续草稿写入或渲染流程

## effect\_mode 选择策略（字幕链路硬约束）

- 只要识别结果将用于“字幕制作 / 模板字幕 / 上屏字幕 / 草稿写回”，必须使用 `nlp`
- 在字幕链路中，禁止使用 `basic` 结果直接写字幕
- 若用户在字幕场景中明确要求 `basic`，也要先说明风险并改为 `nlp` 执行
- `basic` 仅可用于“临时预览、粗转写、非上屏分析”等不进入字幕生产链路的场景

## 适用场景

- 用户要做音视频字幕识别、转写台词
- 用户要拿到时间轴分段 `segments` 用于字幕或检索
- 用户希望控制处理强度：`basic|nlp`（但字幕上屏链路固定 `nlp`）
- 用户提供目标文案，需要做 `sta`（文案对齐）模式

## 输入约束

- `url` 必须是服务端可访问的 `http/https` 链接
- 若用户只给本地路径，先调用 `sts-upload`，再用上传后的 URL 识别

## 视频前置提取（建议默认开启）

- 在 `llm-asr` 执行前，先判断输入是否为视频 URL（如 `.mp4/.mov/.mkv...`）
- 若是视频，优先调用 `extract-audio` 技能提取 `audio.public_url`，再把音频 URL 送入 ASR
- 这样可减少视频解复用开销，通常能提升识别吞吐与稳定性
- 若提取失败，再回退到原视频 URL 继续 ASR，并在结果中记录降级信息

## 前置条件

- Python 3
- 已安装 `requests`
- 环境变量 `VECTCUT_API_KEY` 已设置为可用 token
- 若未设置 `VECTCUT_API_KEY`，必须先调用 `vectcut-login` skill 完成登录与 token 校验，再继续本技能流程

## 执行方式

仅识别（ASR，默认推荐 `nlp`）：

```bash
python <skill-path>/scripts/llm_asr_async.py "https://example.com/video.mp4" --effect-mode nlp --output "./subtitle_editable.json"
```

字幕上屏场景（必须）：

```bash
python <skill-path>/scripts/llm_asr_async.py "https://example.com/video.mp4" --effect-mode nlp --output "./subtitle_editable.json"
```

文案对齐（STA）：

```bash
python <skill-path>/scripts/llm_asr_async.py "https://example.com/video.mp4" --effect-mode nlp --content "你的目标文案" --output "./subtitle_editable.json"
```

可选参数：

- `--poll-interval`：轮询间隔秒数，默认 `2.0`
- `--timeout`：总超时秒数，默认 `600`
- `--auto-extract-audio / --no-auto-extract-audio`：是否自动做视频抽音频前置，默认开启

## 处理流程

1. 若输入像视频 URL，先执行 `extract-audio`（提交 + 轮询）
2. `POST /llm/asr/asr_llm/submit_task/submit_asr_llm_task` 提交任务，拿 `task_id`
3. 轮询 `.../task_status`（默认 GET；必要时自动回退 POST）
4. `status=success` 后读取 `result.content` 与 `result.segments`
5. 落盘为可编辑 JSON

## 输出 JSON

默认输出 `subtitle_editable.json`，主要字段：

- `meta`：来源 URL、任务 id、状态、模式、effect\_mode、生成时间
- `meta.asr_input_url`：ASR 实际使用的输入 URL（可能是提取后的音频 URL）
- `meta.preprocessing`：前置处理信息（是否用了 extract-audio、对应 task\_id 等）
- `full_text`：完整文本（`result.content`）
- `editable_subtitles`：可编辑字幕列表（由 `segments` 转换）
- `raw_result`：原始 `result`，便于复核

`editable_subtitles` 每项字段：

- `id`
- `start_ms`
- `end_ms`
- `text`

## 错误处理建议

- `缺少参数 url`：补充可访问 URL
- `effect_mode 非法`：仅可用 `basic|nlp`
- `字幕链路误用 basic`：立即废弃该结果并使用 `nlp` 重新识别后再上屏
- `余额不足`：充值后重试
- `VECTCUT_API_KEY` 缺失：先调用 `vectcut-login` 完成登录后再重试
- 轮询超时：增大 `--timeout` 或检查源文件可访问性

## 人工修订建议

- 可直接修改 `editable_subtitles[].text` 做错别字修订和润色
- 修改时保持 `start_ms/end_ms` 的时间轴合理
- 仅 `nlp` 结果修订后可作为后续字幕上屏输入；`basic` 结果不得直接用于上屏

## 完成后衔接（llm-asr -> asr-vad）

- 识别完成后，若素材是口播或用户提到“去气口/删嗯啊呃/精剪口播”，主动追问是否继续去气口
- 若用户确认，转到 `asr-vad` 技能：
  - 第一步：按语义规则标记 `keep/drop`
  - 第二步：基于词级时间重建新字幕并生成 `add_video(start/end/target_start)` 片段工作流
  - 然后用 `query-draft` 检查字幕与视频是否对齐、片段是否连续
