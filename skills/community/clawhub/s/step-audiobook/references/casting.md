# Audiobook Casting

语言切换：当前为中文｜[English companion](./casting.en.md)

`recommend_casting.py` 的职责是：把结构化剧本里的角色，映射到统一音色候选池中的一个“当前生效音色”，同时把待确认的付费 clone 单独列出来。

## 阅读导航 / Reading Guide

- 想看总入口与全局约定：回到 `../SKILL.md`
- 想看完整执行顺序：读 `./workflows.md`
- 想先理解结构化剧本来源：读 `./script-format.md`
- 想看下游 TTS 请求和合成：读 `./synthesis.md`

如果你是第一次看角色选角逻辑，推荐阅读顺序是：

1. `../SKILL.md`
2. `./voice-library.md`
3. `./script-format.md`
4. 当前这份 `./casting.md`

## 输入文件

选角依赖 2 个输入：

1. 结构化剧本
2. 统一音色候选池

默认路径：

- 剧本：`~/.openclaw/workspace/runs/audiobook/<slug>/<base>.structured-script.yaml`
- 候选池：`~/.openclaw/workspace/audiobook-library/.audiobook/voice-candidate-pool.yaml`

统一音色候选池是唯一的音色输入源。不要在选角阶段直接回读 `voice-reviews.yaml` 或 `voice-library.yaml` 做匹配。

## 输出文件

`recommend_casting.py` 默认会生成 5 份结果：

- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.casting-review.yaml`
- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.casting-plan.yaml`
- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.clone-review.yaml`
- `~/.openclaw/workspace/runs/audiobook/<slug>/.audiobook/<base>.casting-plan.role-profiles.json`
- `~/.openclaw/workspace/runs/audiobook/<slug>/.audiobook/<base>.casting-plan.casting-selection.json`

它们的角色分别是：

### `casting-review.yaml`

人工确认入口。

这里可以手动改：

- 某个角色最终选哪一个候选音色
- 某个角色的稳定 instruction
- 选角备注

### `casting-plan.yaml`

真正生效的选角结果。

后续 `build_tts_requests.py` 读取的是这份文件，而不是 `casting-review.yaml`。

### `clone-review.yaml`

专门给付费 clone 决策使用。

这里会汇总：

- 哪些角色强烈依赖某个 clone
- 该 clone 是否需要真正付费复刻
- 用户最后的 `confirm_clone / skip / pending`

注意：这份文件本身还不是付费 clone 的直接输入。真正会被 `clone_selected_voices.py` 读取的，是同步回 `voice-library.yaml` 之后的 `selected_for_clone=true` 条目。

### `role-profiles.json`

LLM 为角色抽取的声音画像与证据。

适合排查“角色为什么被理解成这种声音需求”。

### `casting-selection.json`

LLM 选角返回的原始归档。

适合排查“模型为什么选了这个候选”。

## 当前的选角原则

### 原则 1：只用统一音色候选池做匹配

统一音色候选池里混合了两类音色：

- `source=official`
- `source=clone`

选角阶段不再各自走两套逻辑。

### 原则 2：官方音色不要按名字猜语义

官方音色真正用于选角的是这些字段：

- `official_description`
- `recommended_scenes`
- `selection_summary`
- `information_quality`

`display_name` 只用于展示，不应该作为主要依据。

如果某个官方音色缺少描述和推荐场景，它会被标记为 `information_quality=missing`，默认只应作为低信息备选。

### 原则 3：clone 音色读取的是生效画像

clone 候选的主要信息来自：

- `.audiobook/effective-voice-library.yaml`
- 再合并进 `.audiobook/voice-candidate-pool.yaml`

也就是说，clone 的实际选角依据是：

- `description`
- `tags`
- `suitable_scenes`
- `avoid_scenes`
- `stable_instruction`
- `selection_summary`

而这套生效画像本身遵循：

```text
manual > archived_analysis > empty
```

### 原则 4：尽量优先 ready 音色

如果官方 ready 音色和某个待 clone 的候选拟合度接近，系统默认应优先 ready 音色。

只有当某个 clone 明显更贴角色时，才会把它推入 `clone-review.yaml`，让用户决定是否真的付费复刻。

## 当前的 LLM 行为来源

选角默认使用 `voice-library.yaml` 顶层的 LLM 配置：

- `llm.defaults`
- `llm.tasks.casting_role_extraction`
- `llm.tasks.casting_selection`

这意味着：

- 默认是 Step 3.5
- 当前默认的 `step-3.5` 调用走的是 Step 的 `step_plan` 推理接口
- 默认 endpoint 为 `https://api.stepfun.com/step_plan/v1`
- 但后续可以切到别的 OpenAI-compatible 模型
- 文档和代码都尽量避免把规则写死成大量正则 + 权重打分

## 人工确认后如何刷新

### 改了 `casting-review.yaml`

```bash
python3 scripts/recommend_casting.py --library ~/.openclaw/workspace/audiobook-library/voice-library.yaml --input /绝对路径/structured-script.yaml --refresh-only
```

### 改了 `clone-review.yaml`

同样执行：

```bash
python3 scripts/recommend_casting.py --library ~/.openclaw/workspace/audiobook-library/voice-library.yaml --input /绝对路径/structured-script.yaml --refresh-only
```

刷新时会同步：

- 重建 `casting-plan.yaml`
- 重建 `clone-review.yaml`
- 把 `confirm_clone / skip` 回写到 `voice-library.yaml -> selected_for_clone`

也就是说：每次你手工改完 `clone-review.yaml`，都必须先跑这一步，再去执行 `clone_selected_voices.py`。

## 下游继续前的检查项

进入 `build_tts_requests.py` 之前，至少确认：

- 每个真正要发声的角色在 `casting-plan.yaml` 里都有 `selected_voice_id`
- `selected_status=ready`
- 没有仍然停留在“需付费 clone 才能发声”的角色

如果这些条件不满足，`build_tts_requests.py` 会直接报错停止，而不是生成一个残缺的请求清单。
