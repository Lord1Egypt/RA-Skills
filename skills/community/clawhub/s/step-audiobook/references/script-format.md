# Audiobook Script Format

语言切换：当前为中文｜[English companion](./script-format.en.md)

`audiobook` 的下游链路只接受结构化剧本。原始小说 `txt` 需要先通过 `generate_structured_script.py` 转成结构化 YAML。

## 阅读导航 / Reading Guide

- 想看总入口与全局约定：回到 `../SKILL.md`
- 想看完整执行顺序：读 `./workflows.md`
- 想看选角如何使用结构化剧本：读 `./casting.md`
- 想看下游 TTS 请求如何从剧本生成：读 `./synthesis.md`

如果你是第一次处理原始文本到结构化剧本，推荐阅读顺序是：

1. `../SKILL.md`
2. `./workflows.md`
3. 当前这份 `./script-format.md`
4. 再进入 `./casting.md`

## 输入类型总览

当前支持三种故事输入形态：

1. 原始 `txt`
2. 结构化 `yaml`
3. 结构化 `json`

其中：

- `txt`：先跑 `generate_structured_script.py`
- `yaml/json`：可以直接进入 `recommend_casting.py` 或 `build_tts_requests.py`

补充说明：

- `txt -> structured-script` 这一步当前默认使用的是 `step-3.5`
- 当前默认的 `step-3.5` 调用走的是 Step 的 `step_plan` 推理接口
- 默认 endpoint 为 `https://api.stepfun.com/step_plan/v1`
- 如果你在 `voice-library.yaml -> llm.tasks.script_generation` 下改了 `provider / model / base_url`，这一环节可以按配置切换

## 原始 txt 的输出位置

```bash
python3 scripts/generate_structured_script.py --input /绝对路径/小说.txt
```

默认输出：

- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.structured-script.yaml`
- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.structured-script.generation.json`

第一份是后续真正使用的结构化剧本，第二份是生成过程归档。

`structured-script.generation.json` 现在除了归档外，还承担两件事：

- 记录 overview / chunk / finalization 的完整 trace
- 在 `txt -> structured-script` 中断后，作为 chunk 级 resume checkpoint

也就是说，如果长文本在第 N 个 chunk 失败，修好网络或参数后，重新执行同一条 `generate_structured_script.py` 命令，默认会优先尝试从兼容 checkpoint 继续，而不是从头重跑全部 chunk。

如果你把现成的结构化 `yaml/json` 直接传给 `run_audiobook.py --story-input`，脚本会先把它复制到 `~/.openclaw/workspace/runs/audiobook/<slug>/`，这样后续的 `casting-plan`、`tts-requests`、`artifacts.json` 都会和这次 run 放在同一个目录里。

## `examples/` 里的最小脚本示例

skill 自带两份和剧本相关的参考文件：

- `examples/story-minimal.txt`
- `examples/story-minimal.structured-script.yaml`

它们演示的是同一个小场景：雨后巷口、旁白 + 两个角色、少量对白。

建议这样使用：

- 想看 `txt -> structured-script` 的目标形态：对照这两份文件阅读
- 想手工写自己的结构化剧本：从 `story-minimal.structured-script.yaml` 复制后再改
- 想给程序对接字段：直接按这个 YAML 的 `characters + segments` 结构生成

这两份文件是参考样例，不是运行时唯一来源；真正执行时，推荐把你自己的故事文件放进 `~/.openclaw/workspace/audiobook-stories/`。

## 长文本的切块与超时控制

`generate_structured_script.py` 现在默认会做三层保护：

1. 按段落/句子切成基础块
2. 如果识别到 `第X章 / Chapter X / 序章 / 尾声` 这类标题，优先按章节预切，再在章节内继续 chunk
3. 每个 LLM 请求都使用独立 `timeout_seconds`

默认情况下：

- 中断后自动 resume
- 章节预切默认开启
- 单次 LLM HTTP timeout 默认 180 秒

如果你明确不想复用 checkpoint，可以在命令里加：

```bash
python3 scripts/generate_structured_script.py --input /绝对路径/小说.txt --no-resume
```

## 支持的结构化剧本形态

`build_tts_requests.py` 支持两种结构：

1. `characters + dialogues`
2. `characters + segments`

## 形态 A：`characters + dialogues`

适合手写成本最低的场景。

```yaml
title: 示例
global_instruction: 场景=都市夜路｜旁白=中立清晰｜对白=自然克制
characters:
  - id: narrator
    name: 旁白
    instruction: 中立清晰的旁白叙述
  - id: hero
    name: 主角
    instruction: 成年男性，表达自然克制

dialogues:
  - speaker: narrator
    text: 他停下脚步，看向巷子深处。
  - speaker: hero
    text: "（压低声音）不对劲。"
```

最低要求：

- `characters[].id` 必填
- `dialogues[].speaker` 必填
- `dialogues[].text` 必填

自动行为：

- 以 `（...）` 开头的文本会被拆成 `inline_instruction + clean_text`
- `speaker=narrator` 默认 `delivery_mode=narration`
- 其他角色默认 `delivery_mode=dialogue`

## 形态 B：`characters + segments`

适合你想显式控制运行时字段。

```yaml
title: 示例
global_instruction: 场景=悬疑夜路｜旁白=中立清晰｜对白=自然克制
characters:
  - id: narrator
    name: 旁白
    instruction: 中立清晰的旁白叙述
  - id: hero
    name: 主角
    instruction: 成年男性，表达自然克制

segments:
  - index: 0
    speaker: narrator
    raw_text: 他停下脚步，看向巷子深处。
    delivery_mode: narration
  - index: 1
    speaker: hero
    raw_text: "（压低声音）不对劲。"
    delivery_mode: inner_monologue
    scene_instruction: 巷口安静，贴近耳语感
```

可用字段：

- `speaker`：必填
- `raw_text / text / tts_input_text / clean_text`：至少提供一个
- `delivery_mode`：可选，支持
  - `narration`
  - `dialogue`
  - `inner_monologue`
- `inline_instruction`：可选
- `scene_instruction`：可选
- `character_instruction`：可选
- `metadata`：可选对象

## 运行时规范化结果

不管你提供的是 `dialogues` 还是 `segments`，在生成 TTS 请求前都会先统一成：

```text
~/.openclaw/workspace/runs/audiobook/<slug>/<base>.script-runtime.json
```

这份 runtime 文件是自动生成的，不建议人工长期维护。它的作用是：

- 统一 `speaker / character_name / delivery_mode`
- 拆分 `raw_text / clean_text / inline_instruction`
- 补齐缺失角色占位信息

## `global_instruction` 的推荐写法

推荐把全局朗读要求写成稳定、可复用的约束，例如：

```text
场景=都市夜路｜旁白=中立清晰｜对白=自然克制
```

不推荐写法：

- 整段剧情摘要
- 和某一段局部情绪强绑定的指令
- 会和角色长期声线冲突的描述

## 对程序调用者的建议

如果你是程序而不是人工编辑者，建议这样使用：

1. 输入 `txt`，拿 `generate_structured_script.py` 的 stdout JSON
2. 读取它给出的 `output_path`
3. 后续统一用这个 `structured-script.yaml` 继续跑 casting / tts

这样可以避免自己推导 `<slug>` 和 `<base>`。
