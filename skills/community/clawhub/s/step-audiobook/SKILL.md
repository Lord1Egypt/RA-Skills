---
name: audiobook
description: Use when your agent needs to build, maintain, or run the local `audiobook` skill for voice-library management, Step official voice sync, clone voice analysis, LLM casting, replayable TTS requests, segment synthesis, and final audiobook export.
metadata:
  {
    "openclaw":
      {
        "emoji": "🎧",
        "requires": { "bins": ["ffmpeg", "ffprobe"], "env": ["STEP_API_KEY"] },
        "primaryEnv": "STEP_API_KEY",
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "ffmpeg",
              "bins": ["ffmpeg", "ffprobe"],
              "label": "Install ffmpeg / ffprobe (brew)",
            },
          ],
      },
  }
---

# Audiobook

语言切换：当前为中文｜[English companion](./SKILL.en.md)

`audiobook` 是一套完整的本地有声书工作流，覆盖 4 个阶段：

1. 音色库维护：官方音色同步、用户参考音频分析、付费 clone 准备
2. 剧本准备：`txt -> structured-script`
3. 角色选角：`structured-script -> casting-review -> casting-plan`
4. 合成导出：`casting-plan -> tts-requests -> segments -> final audio`

它面向两类调用者：

- 人类用户：按步骤查看和修改中间产物
- 程序调用：读取各脚本的 JSON stdout，以及统一的 `artifacts.json`

`audiobook` 不只是“把小说读出来”的 TTS 工具，而是一套围绕音色资产、结构化剧本、角色选角、可重放 TTS 请求和最终音频导出的完整本地工作流。

它的设计原则是：

- Step 专属能力继续使用 Step 的原生接口，例如 `step-audio-r1.1`、官方音色接口、音色复刻接口、`stepaudio-2.5-tts`
- 需要长文本理解、角色分析、选角推理的部分，默认使用 `step-3.5`
- 当前默认的 `step-3.5` 调用走的是 Step 的 `step_plan` reasoning 接口，默认 endpoint 为 `https://api.stepfun.com/step_plan/v1`
- 上述 LLM 理解层尽量通过可配置的兼容层实现，便于后续按需替换为其他兼容的 LLM
- 各阶段中间产物默认落盘，既方便人工审阅和修改，也方便程序按阶段接续执行

## 能力范围

`audiobook` 当前覆盖以下能力：

1. 用户可以自行准备一批待克隆音色参考音频；skill 会调用 `step-audio-r1.1` 对这些音频做声音特点分析，沉淀成后续角色选角可用的基础画像。
2. 用户可以在分析结果基础上，挑选自己认可的候选音色，显式决定是否在 StepFun 开放平台上执行真正的音色复刻；这一步属于付费动作，不会在默认流程中被自动触发。
3. skill 会自动整合 StepFun 官方系统音色、用户已经完成复刻的音色，以及用户本地维护的待确认音色分析结果，形成统一的音色库与统一音色候选池。
4. 基于用户提供的一套原始文本文件，skill 会默认使用 `step-3.5` 做分块、章节感知、角色分析和结构化整理，生成一个包含旁白在内的 `characters + structured-script` 剧本结果；当前默认使用的就是 Step 的 `step_plan` 推理接口。
5. 基于结构化剧本和统一音色库，skill 会进一步产出一套角色与音色整合后的选角方案；这类依赖语义理解和推理的环节默认使用 `step-3.5`，但整体实现尽量不依赖写死的 NLP 规则，而是通过可替换的 LLM 配置层完成，便于后续切换到其他兼容 LLM。
6. 基于选角结果，skill 会生成一份符合 `stepaudio-2.5-tts` 调用习惯的可重放 TTS 请求清单，便于后续批量合成、局部重跑和参数调整。
7. skill 支持按段合成音频，并将多个 segment 进一步拼接为一个或多个最终音频文件，包括整本导出和局部试听导出。
8. 上述各阶段的关键中间产物都允许用户人工介入修改；用户既可以按步骤审阅，也可以在修改后从某个中间阶段继续重跑，而不必每次都从头开始。

## 术语约定

- 结构化剧本：对应英文 `structured script`
- 统一音色候选池：对应英文 `unified voice candidate pool`
- 生效画像：对应英文 `effective profile`，即 clone 音色真正参与选角的描述集合
- 付费 clone：对应英文 `paid clone`，即真正调用 Step 音色复刻接口的动作
- 中间产物：对应英文 `intermediate artifacts`
- 人工确认：对应英文 `human review` 或 `manual confirmation`
- ready 音色：对应英文 `ready voice`，表示当前已经可以直接进入下游 TTS

## LLM 可替换边界

当前需要重点说明的是：并不是整个 skill 的所有能力都可以替换成别的模型。

- 默认可替换的部分：长文本结构化、角色提取、选角推理等 LLM 理解环节
- 这些环节当前默认使用 `step-3.5`，且默认走 `https://api.stepfun.com/step_plan/v1`
- 默认不替换的部分：`step-audio-r1.1` 音频分析、Step 官方音色拉取、Step 音色复刻、`stepaudio-2.5-tts` 合成
- 也就是说，`audiobook` 当前是“Step 音频能力 + 可替换 LLM 推理层”的组合架构，而不是把所有能力都抽象成完全可替换的通用 provider

## 默认路径

下面这些路径是当前 skill 的默认约定：

```bash
WORKSPACE_ROOT=~/.openclaw/workspace
SKILL_ROOT=$WORKSPACE_ROOT/skills/audiobook
EXAMPLES_ROOT=$SKILL_ROOT/examples
VOICE_LIBRARY=$WORKSPACE_ROOT/audiobook-library/voice-library.yaml
LIBRARY_ROOT=$WORKSPACE_ROOT/audiobook-library
STORY_ROOT=$WORKSPACE_ROOT/audiobook-stories          # 推荐放原始 txt / yaml / json
RUN_ROOT=$WORKSPACE_ROOT/runs/audiobook
```

下面所有命令示例默认都在 `"$SKILL_ROOT"` 目录里执行。也就是说，推荐先：

```bash
cd "$SKILL_ROOT"
```

如果你不想切换目录，请把文档里的 `scripts/<name>.py` 改成对应脚本的绝对路径。

关键位置：

- 音色库入口：`$VOICE_LIBRARY`
- 用户待分析音频投递区：`$LIBRARY_ROOT/voices/inbox/`
- 长期参考音频目录：`$LIBRARY_ROOT/voices/references/<asset_id>/`
- 音色分析 / cache / 统一音色候选池：`$LIBRARY_ROOT/.audiobook/`
- 每本书的中间产物与最终产物：`$RUN_ROOT/<slug>/`
- 轻量参考示例：`$EXAMPLES_ROOT/`

推荐但不强制：把原始小说文件统一放在 `~/.openclaw/workspace/audiobook-stories/`。脚本支持任意绝对路径输入，但统一目录更方便程序化管理。

## 运行前准备

在执行任何主流程前，确保：

- 环境里有 `STEP_API_KEY`
- 系统已安装 `ffmpeg`
- 最终导出或时长探测时，系统已安装 `ffprobe`

## 安全与付费提示

- `audiobook` 现在建议显式调用，不建议依赖隐式注入；这是一个会读写本地文件、并可能访问外部 API 的工作流型 skill。
- 默认的音频分析、官方音色、音色复刻、TTS 合成都会访问 Step 相关接口；长文本理解层如果你改了 `voice-library.yaml -> llm.*.base_url`，则会访问你自己配置的兼容 LLM endpoint。
- 建议优先使用测试 key、受限 key，或至少在第一次运行后做轮换；如果你不完全信任当前配置，先在隔离环境或沙箱里跑一遍。
- `ffmpeg` / `ffprobe` 请只从可信来源安装。
- 真正可能触发付费的只有 `clone_selected_voices.py`；而且现在除了 `selected_for_clone=true` 之外，还必须显式传入 `--confirm-paid-action` 才会执行正式 clone。
- `run_audiobook.py` 默认只会对 clone 阶段做 `--dry-run` 预览，不会自动代替你执行正式付费 clone。
- 如果你在做安全审查，或想确认默认会访问哪些 endpoint、会读取哪些环境变量，直接看 `references/security.md`。

如果本地还没有 `voice-library.yaml`，先用模板初始化：

```bash
mkdir -p "$LIBRARY_ROOT"
cp \
  "$SKILL_ROOT/assets/voice-library.template.yaml" \
  "$VOICE_LIBRARY"
```

如果你希望在第一次 ingest 前就看到带注释的人工审核骨架，也可以顺手初始化：

```bash
cp \
  "$SKILL_ROOT/assets/voice-reviews.template.yaml" \
  "$LIBRARY_ROOT/voice-reviews.yaml"
```

## 最小示例

`examples/` 目录现在提供 7 个轻量示例，适合先理解结构，再复制到自己的工作区继续改：

- `examples/story-minimal.txt`：最小原始小说文本
- `examples/story-minimal.structured-script.yaml`：对应的最小结构化剧本
- `examples/voice-library.minimal.yaml`：最小音色库配置示例
- `examples/voice-reviews.minimal.yaml`：最小人工审核示例
- `examples/story-minimal.casting-plan.yaml`：最小可下游继续的选角结果示例
- `examples/story-minimal.tts-requests.json`：最小可 replay 的 TTS 请求示例
- `examples/story-minimal.script-runtime.json`：由 `build_tts_requests.py` 生成的规范化剧本 companion

使用原则：

- 真正初始化库文件时，优先复制 `assets/*.template.yaml`
- `examples/*minimal*` 更适合“照着看结构”“复制局部片段”“给程序做字段对齐”
- `examples/*.json` / `*.yaml` 里的路径字段已经改成 `$EXAMPLES_ROOT` / `$RUN_ROOT` 占位，不包含本机绝对路径
- 不建议把 `examples/voice-library.minimal.yaml` 直接当成长期运行时库文件

## 最常用的入口

一次性跑完整主流程时，优先用：

```bash
python3 scripts/run_audiobook.py --library "$VOICE_LIBRARY" --story-input /绝对路径/小说.txt
```

这条命令会按顺序尝试：

1. 刷新官方音色 cache
2. 处理 `--voice-input` 或 `--process-inbox` 指定的新音频
3. 如果输入是 `txt`，先生成 `structured-script`
4. 生成 `casting-review`、`casting-plan`、`clone-review`
5. 预览本次哪些 clone 值得付费复刻
6. 当角色和 clone 状态允许继续时，再进入 `tts-requests -> synthesize -> finalize`

如果你要分步执行，建议顺序见 `references/workflows.md`。

## 推荐命令顺序

### 1. 音色库同步 / 音频分析

分析单条音频：

```bash
python3 scripts/sync_voice_library.py --library "$VOICE_LIBRARY" --input /绝对路径/参考音频.m4a
```

批量处理投递区：

```bash
python3 scripts/run_audiobook.py --library "$VOICE_LIBRARY" --story-input /绝对路径/小说.txt --process-inbox
```

只想批量处理投递区，不进入故事链路：

```bash
python3 scripts/run_audiobook.py --library "$VOICE_LIBRARY" --process-inbox --downstream-mode off
```

仅刷新官方音色：

```bash
python3 scripts/sync_voice_library.py --library "$VOICE_LIBRARY" --refresh-official-only
```

快速列出仍待人工确认的 clone 音色：

```bash
python3 scripts/list_pending_reviews.py --library "$VOICE_LIBRARY" --pretty
```

### 2. 原始小说转结构化剧本

```bash
python3 scripts/generate_structured_script.py --library "$VOICE_LIBRARY" --input /绝对路径/小说.txt
```

默认输出：

```text
~/.openclaw/workspace/runs/audiobook/<slug>/<base>.structured-script.yaml
```

### 3. 生成角色选角结果

```bash
python3 scripts/recommend_casting.py --library "$VOICE_LIBRARY" --input /绝对路径/structured-script.yaml
```

默认输出：

- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.casting-review.yaml`
- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.casting-plan.yaml`
- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.clone-review.yaml`
- `~/.openclaw/workspace/runs/audiobook/<slug>/.audiobook/<base>.casting-plan.role-profiles.json`
- `~/.openclaw/workspace/runs/audiobook/<slug>/.audiobook/<base>.casting-plan.casting-selection.json`

### 4. 构建可重放的 TTS 请求

```bash
python3 scripts/build_tts_requests.py --input /绝对路径/structured-script.yaml
```

默认输出：

- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.script-runtime.json`
- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.tts-requests.json`

### 5. 实际合成分段音频

```bash
python3 scripts/synthesize_tts_requests.py --input /绝对路径/<base>.tts-requests.json
```

默认输出：

- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.segments/`

### 6. 导出整本或试听片段

```bash
python3 scripts/finalize_audiobook.py --input /绝对路径/<base>.tts-requests.json
```

默认整本输出：

```text
~/.openclaw/workspace/runs/audiobook/<slug>/<base>.audiobook.wav
```

如果你把 `response_format` 改成 `mp3 / flac / opus`，最终扩展名会跟着变化。默认值仍然是 `wav`。

如果只导出部分片段，会输出：

```text
~/.openclaw/workspace/runs/audiobook/<slug>/<base>.preview-<segments>.<response_format>
```

## 中间产物怎么查看

每本书都有一份统一清单：

```text
~/.openclaw/workspace/runs/audiobook/<slug>/<base>.artifacts.json
```

它会列出：

- 源文本 / 结构化剧本
- 选角审核与生效结果
- 音色库侧的 `voice-reviews`、`effective-voice-library`、`voice-candidate-pool`、`official-voices-cache`
- `script-runtime`、`tts-requests`
- `segments/`
- 最近一次导出与最终成品

人类查看时：

```bash
python3 scripts/list_story_artifacts.py --manifest /绝对路径/<base>.artifacts.json --level review --pretty
```

程序调用时：直接读取 `artifacts.json` 即可，不需要硬编码路径推导。

如果你只想快速看音色库里还有哪些 clone 描述待人工确认，用：

```bash
python3 scripts/list_pending_reviews.py --library "$VOICE_LIBRARY" --pretty
```

## 哪些文件可以改，哪些文件不要改

建议人工编辑的文件：

- `voice-reviews.yaml`
- `*.casting-review.yaml`
- `*.clone-review.yaml`
- `*.structured-script.yaml`
- `*.tts-requests.json`

不建议直接编辑的生成文件：

- `.audiobook/effective-voice-library.yaml`
- `.audiobook/voice-candidate-pool.yaml`
- `.audiobook/official-voices-cache.json`
- `*.casting-plan.yaml`（除非你明确知道自己在做什么）
- `*.script-runtime.json`
- `*.artifacts.json`

改完后的重跑命令见 `references/editing.md`。

## 两套 `.audiobook/` 的区别

这是最容易混淆的点：

- `~/.openclaw/workspace/audiobook-library/.audiobook/`：音色库侧生成文件
- `~/.openclaw/workspace/runs/audiobook/<slug>/.audiobook/`：某本书本次运行的 trace / debug 文件

前者服务整个音色库；后者只服务单次故事流程。

## 付费边界

`clone_selected_voices.py` 是唯一会触发付费 clone 的步骤。默认流程只会：

- 分析参考音频
- 生成 clone 候选
- 在 `clone-review.yaml` 里等待确认

真正执行前请先跑：

```bash
python3 scripts/clone_selected_voices.py --library "$VOICE_LIBRARY" --dry-run
```

正式执行时，现在必须额外确认：

```bash
python3 scripts/clone_selected_voices.py --library "$VOICE_LIBRARY" --confirm-paid-action
```

## 机器可读接口

下面这些脚本都输出 JSON 到 stdout，适合程序调用：

- `sync_voice_library.py`
- `generate_structured_script.py`
- `recommend_casting.py`
- `build_tts_requests.py`
- `synthesize_tts_requests.py`
- `finalize_audiobook.py`
- `run_audiobook.py`

对程序来说，最稳的组合是：

1. 调主脚本拿 stdout JSON
2. 再读取 `artifacts.json` 拿完整文件清单

## 参考文档索引 / Reference Index

如果你是人类用户，建议优先看中文；如果你是英文环境下的 agent 或程序，可直接读对应的英文 companion 文档。

- 完整执行顺序 / full workflow：中文 `references/workflows.md`｜English `references/workflows.en.md`
- 音色库结构与字段 / voice library structure：中文 `references/voice-library.md`｜English `references/voice-library.en.md`
- 结构化剧本格式 / structured script format：中文 `references/script-format.md`｜English `references/script-format.en.md`
- 选角规则与输出 / casting rules and outputs：中文 `references/casting.md`｜English `references/casting.en.md`
- TTS、replay 与最终导出 / synthesis and export：中文 `references/synthesis.md`｜English `references/synthesis.en.md`
- 人工修改与重跑 / manual editing and reruns：中文 `references/editing.md`｜English `references/editing.en.md`
- 安全与外部访问 / security and external access：中文 `references/security.md`｜English `references/security.en.md`

如果你只是想快速进入某个主题，推荐顺序是：

1. 想看整体链路：先读 `references/workflows.md`
2. 想维护音色库：再读 `references/voice-library.md`
3. 想修改中间产物：直接读 `references/editing.md`
