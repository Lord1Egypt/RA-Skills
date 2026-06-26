---
name: describe-video
description: "在剪辑开始前批量读取并理解所有素材：先提取音频，再用 basic 模式提取字幕与分句时间戳，再做视频画面内容理解，最后产出可直接用于剪辑决策的结构化素材文档。用户提到“先看素材里有什么/素材盘点/口播+B-roll可用性分析/是否要剪气口/先做视频理解”时必须使用本技能。注意：本技能输出仅用于分析，不能直接用于字幕上屏。"
---

# Describe Video Skill

用于剪辑前的“素材盘点”与“可剪性分析”。

核心流程固定为四步：
- 第零步：先调用 `get_duration` 获取素材时长，超过 10 分钟（`>600s`）直接拒绝处理
- 第一步：若输入为视频，先调用 `extract-audio` 提取音频 URL
- 第二步：调用识别字幕接口（`basic`）拿到文本与分句时间戳
- 第三步：调用视频理解接口拿到画面细节，并支持自定义 `prompt` 查询关键问题，再整合为结构化文档

## 重要限制（必须遵守）

- 本技能中的 `basic` ASR 结果仅用于“素材分析”和“剪辑决策参考”
- 禁止把本技能输出的 `segments/full_text` 直接用于字幕上屏
- 若后续要做字幕模板/字幕上屏，必须重新调用 `llm-asr` 且 `effect_mode=nlp`
- `llm-asr`（basic）失败不视为任务失败：视频可能无人声，记录该素材“无可用语音/字幕”后继续后续步骤
- `video_detail` 失败不视为任务失败：视频可能无有效画面或解析失败，记录该素材“无可用画面理解结果”后继续

## 适用场景

- 想先看所有素材里“到底有什么内容”
- 想知道每条视频是否是口播、是否需要剪气口
- 想判断口播与其他素材（B-roll）是否能搭配
- 想在进入剪辑前先拿到一份可检索、可复盘的素材说明

## 前置条件

- Python 3
- 已安装 `requests`
- `VECTCUT_API_KEY` 已设置
- 若 `VECTCUT_API_KEY` 缺失或失效，先调用 `vectcut-login` 技能

## 执行方式

单素材：

```bash
python <skill-path>/scripts/describe_video.py "https://example.com/video.mp4"
```

多素材：

```bash
python <skill-path>/scripts/describe_video.py \
  "https://example.com/koubo.mp4" \
  "https://example.com/broll1.mp4" \
  "https://example.com/broll2.mp4" \
  --analysis-prompt "是否出现产品近景、价格信息、操作演示？"
```

从文件读取（每行一个 URL）：

```bash
python <skill-path>/scripts/describe_video.py \
  --input-file "./materials.txt" \
  --analysis-prompt "是否有可做转场或补画面的镜头？"
```

## 关键参数

- `urls...`：一个或多个素材 URL（与 `--input-file` 至少提供一种）
- `--input-file`：素材 URL 文本文件（每行一条）
- `--analysis-prompt`：传给视频理解接口的可选问题（例如“有无产品特写”）
- `--poll-interval`：ASR 轮询间隔秒，默认 `2.0`
- `--timeout`：单条素材 ASR 轮询超时秒，默认 `600`
- `--json-output`：结构化输出文件，默认 `describe_video_report.json`
- `--md-output`：可读文档输出文件，默认 `describe_video_report.md`

## 接口调用约束

- 时长预检（必须先执行）：
  - `POST /cut_jianying/get_duration`（文档：https://docs.vectcut.com/328289318e0）
  - 若返回时长 `>600s`，直接拒绝该素材并返回“超过 10 分钟不处理”
- 音频前置提取（视频输入时默认执行）：
  - `POST /process/extract_audio/submit_task/submit_extract_audio_task`
  - `GET /process/extract_audio/submit_task/task_status` 轮询
- 字幕提取固定使用：
  - `POST /llm/asr/asr_llm/submit_task/submit_asr_llm_task`，`effect_mode=basic`
  - `GET /llm/asr/asr_llm/submit_task/task_status` 轮询
  - 失败按“非致命错误”处理：继续执行 `video_detail` 与报告汇总
- 画面理解使用：
  - `POST /llm/video_detail`
  - 可透传 `prompt` 用于定向检查关键信息
  - 失败按“非致命错误”处理：继续输出其余可用结果

## 输出结果

产出两份文件：

- `describe_video_report.json`：结构化机器可读结果
- `describe_video_report.md`：面向剪辑的快速阅读文档

输出包含：
- 每条素材的字幕摘要、分句时间戳、画面理解结果
- 素材类型判断（口播候选 / B-roll 候选）
- 总体统计（口播数量、可搭配素材数量）
- 剪辑建议（是否建议去气口、是否建议口播+B-roll搭配）
- 错误容忍记录（如“无人声导致 ASR 失败”“无有效画面导致 video_detail 失败”）
