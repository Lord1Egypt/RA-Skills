# Audiobook Workflows

语言切换：当前为中文｜[English companion](./workflows.en.md)

这份文档只回答一件事：从什么输入开始，应该按什么顺序执行 `audiobook`，每一步会产出什么文件。

## 阅读导航 / Reading Guide

- 想看总入口与全局约定：回到 `../SKILL.md`
- 想先理解音色库：读 `./voice-library.md`
- 想直接改中间产物并重跑：读 `./editing.md`
- 想看结构化剧本格式：读 `./script-format.md`
- 想看 TTS 合成与导出：读 `./synthesis.md`

如果你是第一次接触这个 skill，推荐阅读顺序是：

1. `../SKILL.md`
2. `./voice-library.md`
3. 当前这份 `./workflows.md`
4. 再按需进入 `./editing.md` 或 `./synthesis.md`

## 统一路径约定

```bash
WORKSPACE_ROOT=~/.openclaw/workspace
SKILL_ROOT=$WORKSPACE_ROOT/skills/audiobook
VOICE_LIBRARY=$WORKSPACE_ROOT/audiobook-library/voice-library.yaml
LIBRARY_ROOT=$WORKSPACE_ROOT/audiobook-library
STORY_ROOT=$WORKSPACE_ROOT/audiobook-stories          # 推荐
RUN_ROOT=$WORKSPACE_ROOT/runs/audiobook
```

产物路径统一遵循：

- 音色库侧：`$LIBRARY_ROOT/...`
- 单本书侧：`$RUN_ROOT/<slug>/...`

下面所有命令示例默认都在 `"$SKILL_ROOT"` 目录里执行。先执行一次：

```bash
cd "$SKILL_ROOT"
```

补充说明：

- 当前和长文本理解、角色分析、选角推理相关的默认 LLM 都是 `step-3.5`
- 当前默认的 `step-3.5` 调用走的是 Step 的 `step_plan` 推理接口
- 默认 endpoint 为 `https://api.stepfun.com/step_plan/v1`
- 如果你在 `voice-library.yaml -> llm` 下改了 provider / model / base_url，这些理解型环节可以按配置切换

## 流程 A：只维护音色库

适合先准备官方音色和用户参考音频，不急着跑某一本书。

### A1. 初始化或检查音色库

```bash
mkdir -p "$LIBRARY_ROOT"
cp \
  "$SKILL_ROOT/assets/voice-library.template.yaml" \
  "$VOICE_LIBRARY"
```

如果你希望在第一次同步前就先准备好人工审核文件，也可以额外复制：

```bash
cp \
  "$SKILL_ROOT/assets/voice-reviews.template.yaml" \
  "$LIBRARY_ROOT/voice-reviews.yaml"
```

核心文件：

- `~/.openclaw/workspace/audiobook-library/voice-library.yaml`
- `~/.openclaw/workspace/audiobook-library/voice-reviews.yaml`

### A2. 刷新官方音色

```bash
python3 scripts/sync_voice_library.py --library "$VOICE_LIBRARY" --refresh-official-only
```

会更新：

- `~/.openclaw/workspace/audiobook-library/.audiobook/official-voices-cache.json`
- `~/.openclaw/workspace/audiobook-library/.audiobook/effective-voice-library.yaml`
- `~/.openclaw/workspace/audiobook-library/.audiobook/voice-candidate-pool.yaml`

### A3. 分析一条用户参考音频

直接传路径：

```bash
python3 scripts/sync_voice_library.py --library "$VOICE_LIBRARY" --input /绝对路径/参考音频.m4a
```

或先投递到 inbox：

```bash
cp /绝对路径/参考音频.m4a ~/.openclaw/workspace/audiobook-library/voices/inbox/
python3 scripts/sync_voice_library.py --library "$VOICE_LIBRARY"
```

这里要注意：

- `sync_voice_library.py` 在不带 `--input` 时，当前只会消费 `inbox/` 里的 1 条音频
- 如果你想一次性吃掉 `inbox/` 里当前所有文件，建议执行：

```bash
python3 scripts/run_audiobook.py --library "$VOICE_LIBRARY" --process-inbox --downstream-mode off
```

成功后会得到：

- `~/.openclaw/workspace/audiobook-library/voices/references/<asset_id>/raw.<ext>`
- `~/.openclaw/workspace/audiobook-library/voices/references/<asset_id>/reference.wav`
- `~/.openclaw/workspace/audiobook-library/.audiobook/voice-analysis/<asset_id>.json`
- `~/.openclaw/workspace/audiobook-library/voice-reviews.yaml`
- `~/.openclaw/workspace/audiobook-library/.audiobook/effective-voice-library.yaml`
- `~/.openclaw/workspace/audiobook-library/.audiobook/voice-candidate-pool.yaml`

如果输入来自 `voices/inbox/`，原始文件会被消费到 `voices/references/<asset_id>/raw.<ext>`，不会残留在 inbox 里重复处理。

### A4. 人工确认音色描述

编辑：

- `~/.openclaw/workspace/audiobook-library/voice-reviews.yaml`

真正会生效的是：

- `manual`
- 如果 `manual` 某个字段为空，则回落到 `archived_analysis`

改完后刷新：

```bash
python3 scripts/sync_voice_library.py --library "$VOICE_LIBRARY" --asset-id <asset_id> --refresh-profiles-only
```

### A5. 确认真正付费 clone

如果 clone 决策来自某本书的 `clone-review.yaml`，建议先：

1. 把 `items.<asset_id>.manual.decision` 改成 `confirm_clone`
2. 执行 `recommend_casting.py --refresh-only`
3. 确认 `voice-library.yaml -> clones.<asset_id>.selected_for_clone=true`

然后再执行：

```bash
python3 scripts/clone_selected_voices.py --library "$VOICE_LIBRARY" --dry-run
python3 scripts/clone_selected_voices.py --library "$VOICE_LIBRARY" --confirm-paid-action
```

如果你不是从故事级 `clone-review.yaml` 发起，而是直接维护库级配置，也可以直接把 `voice-library.yaml -> clones.<asset_id>.selected_for_clone` 设为 `true`，再执行上面的 dry-run / 正式 clone。

成功后会更新：

- `~/.openclaw/workspace/audiobook-library/.audiobook/voice-registry.json`
- `~/.openclaw/workspace/audiobook-library/.audiobook/effective-voice-library.yaml`
- `~/.openclaw/workspace/audiobook-library/.audiobook/voice-candidate-pool.yaml`

## 流程 B：从原始 txt 到最终音频

这是最完整的故事工作流。

如果你只是想先理解中间产物而不立刻跑真实小说，可以直接先看 `examples/` 里的这条最小链路：

- `story-minimal.txt`
- `story-minimal.structured-script.yaml`
- `story-minimal.casting-plan.yaml`
- `story-minimal.tts-requests.json`

它们分别对应 `txt -> structured-script -> casting-plan -> tts-requests` 四个阶段。

### B1. 直接统一入口

```bash
python3 scripts/run_audiobook.py --library "$VOICE_LIBRARY" --story-input /绝对路径/小说.txt
```

适合：

- 想尽快得到整套中间产物
- 愿意在有 blocker 时停下来人工确认

默认行为：

1. 刷新官方音色
2. 处理新音频（如果传了 `--voice-input` 或 `--process-inbox`）
3. `txt -> structured-script`
4. 生成 `casting-review`、`casting-plan`、`clone-review`
5. 预览待 clone 条目
6. 如果没有 blocker，再继续 `tts-requests -> synthesize -> finalize`

这里的 blocker 主要是：

- clone 音色描述还没人工确认
- 某些角色的最终音色还没人工确认
- 某些角色仍然依赖待付费 clone 的音色

### B2. 分步执行

适合需要频繁人工修改中间产物的场景。

#### 第一步：原始 txt -> structured script

```bash
python3 scripts/generate_structured_script.py --library "$VOICE_LIBRARY" --input /绝对路径/小说.txt
```

这一阶段现在默认具备：

- 章节标题感知的预切分
- chunk 级 checkpoint / resume
- 每个 LLM 请求的独立 timeout
- 默认使用 `step-3.5`，且默认走 `https://api.stepfun.com/step_plan/v1`

输出：

- `$RUN_ROOT/<slug>/<base>.structured-script.yaml`
- `$RUN_ROOT/<slug>/<base>.structured-script.generation.json`

#### 第二步：structured script -> casting

```bash
python3 scripts/recommend_casting.py --library "$VOICE_LIBRARY" --input $RUN_ROOT/<slug>/<base>.structured-script.yaml
```

这一阶段默认也是使用 `step-3.5`，且默认走 `https://api.stepfun.com/step_plan/v1`。

输出：

- `$RUN_ROOT/<slug>/<base>.casting-review.yaml`
- `$RUN_ROOT/<slug>/<base>.casting-plan.yaml`
- `$RUN_ROOT/<slug>/<base>.clone-review.yaml`
- `$RUN_ROOT/<slug>/.audiobook/<base>.casting-plan.role-profiles.json`
- `$RUN_ROOT/<slug>/.audiobook/<base>.casting-plan.casting-selection.json`

#### 第三步：casting -> tts-requests

```bash
python3 scripts/build_tts_requests.py --input $RUN_ROOT/<slug>/<base>.structured-script.yaml
```

输出：

- `$RUN_ROOT/<slug>/<base>.script-runtime.json`
- `$RUN_ROOT/<slug>/<base>.tts-requests.json`

#### 第四步：tts-requests -> segments

```bash
python3 scripts/synthesize_tts_requests.py --input $RUN_ROOT/<slug>/<base>.tts-requests.json
```

输出：

- `$RUN_ROOT/<slug>/<base>.segments/`

#### 第五步：segments -> final audio

```bash
python3 scripts/finalize_audiobook.py --input $RUN_ROOT/<slug>/<base>.tts-requests.json
```

输出：

- `$RUN_ROOT/<slug>/<base>.audiobook.<response_format>`

默认 `response_format=wav`，所以最常见的文件名仍然是 `$RUN_ROOT/<slug>/<base>.audiobook.wav`。

## 流程 C：从已有 structured script 开始

如果你已经有 YAML / JSON 结构化剧本，就不需要先跑 `generate_structured_script.py`。

```bash
python3 scripts/recommend_casting.py --library "$VOICE_LIBRARY" --input /绝对路径/剧本.yaml
python3 scripts/build_tts_requests.py --input /绝对路径/剧本.yaml
python3 scripts/synthesize_tts_requests.py --input $RUN_ROOT/<slug>/<base>.tts-requests.json
python3 scripts/finalize_audiobook.py --input $RUN_ROOT/<slug>/<base>.tts-requests.json
```

注意：`build_tts_requests.py` 只接受结构化 YAML / JSON，不接受原始 txt。

## 流程 D：从任意中间阶段重跑

### 改了 `voice-reviews.yaml`

```bash
python3 scripts/sync_voice_library.py --library "$VOICE_LIBRARY" --asset-id <asset_id> --refresh-profiles-only
```

### 改了 `casting-review.yaml` 或 `clone-review.yaml`

```bash
python3 scripts/recommend_casting.py --library "$VOICE_LIBRARY" --input /绝对路径/structured-script.yaml --refresh-only
```

### 改了 `structured-script.yaml` 或 `casting-plan.yaml`

```bash
python3 scripts/build_tts_requests.py --input /绝对路径/structured-script.yaml
```

### 改了 `tts-requests.json`

全量重放：

```bash
python3 scripts/synthesize_tts_requests.py --input /绝对路径/<base>.tts-requests.json
```

局部重放：

```bash
python3 scripts/synthesize_tts_requests.py --input /绝对路径/<base>.tts-requests.json --segments 1,3-5
```

仅重跑失败段：

```bash
python3 scripts/synthesize_tts_requests.py --input /绝对路径/<base>.tts-requests.json --only-failed
```

### 只导出试听片段

```bash
python3 scripts/finalize_audiobook.py --input /绝对路径/<base>.tts-requests.json --segments 1,3-5
```

## 每轮运行后的统一检查点

不管你是统一入口还是分步执行，都建议最后查看：

```text
$RUN_ROOT/<slug>/<base>.artifacts.json
```

或：

```bash
python3 scripts/list_story_artifacts.py --manifest /绝对路径/<base>.artifacts.json --level review --pretty
```

这份 manifest 是当前最稳定的文件索引入口，适合人类检查，也适合程序对接。
