---
name: universal-video-director
description: 端到端的视频、AI 短剧、漫剧生产流水线：原著分析、剧本、资产锁定、站位、分镜、视频提示词、确认后生产、剪辑合成、评审、循环修复，每个阶段产出一份带 JSON Schema 的标准产物，由校验器检查并标出问题出在哪个阶段。只要用户想做短视频、AI 短剧、漫剧、动态漫、宣传片、解说视频、分镜脚本，想把小说、剧本、创意或素材变成视频，或者想诊断、修复一个已有的视频项目（人物穿帮、跳轴、字幕错、时长不对），都应使用本技能，即使用户没有明说要走完整流程。只剪一段现成素材、只转码、只写一段文案时不需要它。
compatibility: 需要 Python 3.9+（校验器仅用标准库）；剪辑合成需要 ffmpeg/ffprobe；可选 Remotion 或 HyperFrames；生图、生视频、配音、配乐需要用户自备平台账号。
license: MIT（上游借鉴项目各自许可见 references/sources.md）
metadata:
  display_name: 通用视频生成导演
  icon: 🎬
  version: 3.0.0
  inputs:
    idea: 一句话创意、故事梗概、小说文件、已有剧本、参考视频，或已有项目目录
    video_type: drama 短剧 | comic 漫剧(关键帧+配音) | promo 宣传 | explainer 解说 | montage 混剪 | edit 素材剪辑
    duration_sec: 成片目标时长（秒）
    aspect_ratio: 9:16 | 16:9 | 1:1 | 4:5
    target_stage: 做到哪个阶段为止（如只要文字稿就填 video_prompts）；默认 deliver 全流程
    max_repair_rounds: 评审-修复循环最大轮数
---

## Overview
本技能是**总控（orchestrator）**，负责建项目、调度阶段、跑校验、按根因回退。各阶段的创作方法写在 `references/stages/` 下的子技能里，**进入某个阶段时先读对应的子技能文件，再动手**。
设计原则（来自对 12 个开源 skill 的提炼，见 `references/sources.md`）：
1. **一阶段一产物一 schema**：所有决策落到 `project/NN_<stage>.json`，下游只读上游，不在下游打补丁。
2. **软门禁**：校验器只把确定性的机械问题（ID 悬空、时长不等、锁定词缺失、未确认先花钱）判为 ERROR，启发式问题只给 WARNING，交给 Agent 复核。
3. **按需出片**：`render_mode` 设为 video / still / mixed。漫剧默认 mixed，大部分镜头用首帧图加程序化运镜，只有关键动作镜头才生成视频，可以省下大头费用。
4. **锁定再拍**：角色、场景、道具先锁定，锁定词原样贴进每一条提示词；有站位和轴线之后才做分镜。
5. **先预览、确认后再花钱**：所有生图、生视频、配音任务先列清单和预估，用户确认后才提交，并保存平台任务 ID，便于断点续跑。
6. **评审只看渲染出来的帧**，问题标注 `root_stage`；修复从最上游开始，上游改动后用哈希让下游自动失效。

## 阶段与子技能

| # | 阶段 key | 产物文件 | 子技能文件 | 可跳过 |
|---|---|---|---|---|
| 0 | project | `00_project.json` | `references/stages/00-project.md` | 否 |
| 1 | source_analysis | `01_source_analysis.json` | `references/stages/01-source-analysis.md` | 只有一句话创意时 |
| 2 | story | `02_story.json` | `references/stages/02-story.md` | 否 |
| 3 | assets | `03_assets.json` | `references/stages/03-assets.md` | 否 |
| 4 | staging | `04_staging.json` | `references/stages/04-staging.md` | promo/explainer |
| 5 | storyboard | `05_storyboard.json` | `references/stages/05-storyboard.md` | 否 |
| 6 | video_prompts | `06_video_prompts.json` | `references/stages/06-video-prompts.md` | 否（静帧段也在这里写运镜） |
| 7 | production | `07_production.json` | `references/stages/07-production.md` | 否 |
| 8 | edl | `08_edl.json` | `references/stages/08-edit-compose.md` | 否 |
| 9 | qa_report | `09_qa_report.json` | `references/stages/09-review.md` | 否 |
| 10 | repair_log | `10_repair_log.json` | `references/stages/10-repair-loop.md` | 一次通过时 |

Schema 定义在 `assets/schemas/<stage>.schema.json`。所有产物都有公共头部：`schema`、`version`、`stage`、`project_id`、`upstream`（上游文件哈希）。

## 开始前要弄清的输入
开工前从用户的话里提取下面这些信息，缺的用默认值，关键信息缺失时一次性问清楚：
- **idea**：一句话创意、故事梗概、小说文件、已有剧本、参考视频，或已有项目目录
- **video_type**：drama 短剧 | comic 漫剧(关键帧+配音) | promo 宣传 | explainer 解说 | montage 混剪 | edit 素材剪辑（默认 drama）
- **duration_sec**：成片目标时长（秒）（默认 60）
- **aspect_ratio**：9:16 | 16:9 | 1:1 | 4:5（默认 9:16）
- **target_stage**：做到哪个阶段为止（如只要文字稿就填 video_prompts）；默认 deliver 全流程（默认 deliver）
- **max_repair_rounds**：评审-修复循环最大轮数（默认 3）

## Workflow

### Step 1: 诊断或立项
- **Mode**: `agentic`
- **Input**: 用户给的素材、视频类型、目标时长、画幅
- **Output**: 新项目按 `references/stages/00-project.md` 写好 `00_project.json`；已有项目运行 `python scripts/uvd_validate.py all project/`，读取结果里的 `root_cause_stage`（有上游改动时它才是真正要回去修的阶段）、`first_failing_stage`、`next_missing_stage` 和 `stale`
- **Validate**: `00_project.json` 通过 schema 校验
- **On failure**: 缺少主角、平台、生成后端、预算这类信息时，一次性问清楚

### Step 2: 逐阶段推进（循环，直到 用户要求的终点阶段（默认交付成片））
- **Mode**: `agentic`
- **Input**: 当前阶段 key
- **Output**: 该阶段的 JSON 产物，必要时附一份给人看的 Markdown 摘要
- **做法**: 读 `references/stages/<当前阶段>.md`，按里面的方法写产物，然后：
  1. 跑 `uvd_validate.py stage <stage> project/NN_<stage>.json --project project/`；
  2. 有 ERROR 时，`root_stage` 等于当前阶段就原地修，指向上游就回到上游阶段；
  3. 通过后跑 `uvd_validate.py stamp project/ <stage>`，记下上游哈希；
  4. 碰到审批关卡（剧本、资产、花钱）时停下来，等用户确认。
- **Why**: 先做 stamp，上游一改，`stale` 就能精确列出哪些下游需要重做

### Step 3: 评审与修复循环
- **Mode**: `agentic`
- **Input**: 渲染出来的成片
- **Output**: 按 `references/stages/09-review.md` 写 `09_qa_report.json`；没通过就按 `references/stages/10-repair-loop.md` 修复，并在 `10_repair_log.json` 追加记录
- **终止条件**: 校验器确认 `pass=true`，或者修复轮数达到 最大修复轮数（默认 3）

### Step 4: 交付
- **Mode**: `agentic`
- **Input**: 已通过评审（或修复轮数用完）的 `08_edl.json` 和渲染文件，`09_qa_report.json`，`10_repair_log.json`，`07_production.json` 的费用记录
- **Output**: 成片、srt 字幕、封面，以及全部阶段产物。汇报内容包括最终分数、修了几轮、剩余问题、实际花费

## 校验器速查
```
python scripts/uvd_validate.py all project/                 # 全量：first_failing_stage / next_missing_stage / stale
python scripts/uvd_validate.py stage storyboard project/05_storyboard.json --project project/
python scripts/uvd_validate.py stale project/                # 上游变了，哪些需要重做
python scripts/uvd_validate.py stamp project/ storyboard     # 阶段完成后打哈希
```
每条报错都带 `root_stage`、`code`、`msg`、`fix`，修复环节直接拿来用。沙箱里不能运行子进程时，可以 `exec` 这个脚本，再调用 `validate_stage()` 或 `validate_all()`。

## Lessons Learned
### Do
- 进入任何阶段之前，先读它的子技能文件；子技能文件里写的是方法，这份总控文件只管流程
- 锁定词、开场站位句、台词，都要原样复制，不要改写
- 生成任务一提交就保存 task_id；中断以后先 collect 取回结果，不要重复提交
### Don't
- 不要在剪辑阶段修剧情或镜头，也不要只改一个镜头而不检查它前后的 CUT
- 用户没确认，不要调用任何要花钱的接口
### Common Failures
- 模型单次时长上限截断了镜头 → 回到分镜阶段拆 segment（错误码 OVER_MODEL_MAX / SEG_TOO_LONG）
- 跨镜头人物穿帮、换脸 → 回到资产阶段补锚点图和锁定词（LOCK_MISSING / identity_swap）
- 字幕和台词对不上 → 字幕必须逐字取自 story（SUB_NOT_VERBATIM）
- 剧本时长擦边（DURATION_EDGE）→ 在剧本阶段就补足或删减，下游剪辑一压缩就会越界
- 需要模型画汉字或墨迹文字 → 生成画面里不出字，在剪辑阶段用叠层动画呈现（避免 text_garble）
### When to Ask the User
- 剧本定稿、资产定稿、花钱前的确认、选配音和音乐（模型听不出好坏）、修复轮数用完后要不要继续
