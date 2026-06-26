# Audiobook Synthesis

语言切换：当前为中文｜[English companion](./synthesis.en.md)

这份文档说明 `audiobook` 的下游合成链路：`build_tts_requests.py -> synthesize_tts_requests.py -> finalize_audiobook.py`。

## 阅读导航 / Reading Guide

- 想看总入口与全局约定：回到 `../SKILL.md`
- 想看完整执行顺序：读 `./workflows.md`
- 想先理解结构化剧本与选角来源：读 `./script-format.md` 和 `./casting.md`
- 想手工修改请求后重跑：读 `./editing.md`

如果你是第一次关注下游合成，推荐阅读顺序是：

1. `../SKILL.md`
2. `./workflows.md`
3. `./casting.md`
4. 当前这份 `./synthesis.md`

## 路径总览

默认情况下，下游产物都放在：

```text
~/.openclaw/workspace/runs/audiobook/<slug>/
```

关键文件：

- `<base>.script-runtime.json`
- `<base>.tts-requests.json`
- `<base>.segments/`
- `<base>.audiobook.<response_format>`
- `<base>.preview-<segments>.<response_format>`

默认 `response_format=wav`，所以最常见的文件名仍然是 `.wav`。

## 第一步：构建 TTS 请求清单

```bash
python3 scripts/build_tts_requests.py --input /绝对路径/structured-script.yaml
```

## `examples/` 里的最小下游示例

如果你只是想先看下游链路的最小形态，先读这 3 份文件：

- `examples/story-minimal.casting-plan.yaml`
- `examples/story-minimal.tts-requests.json`
- `examples/story-minimal.script-runtime.json`

它们和前面的 `story-minimal.structured-script.yaml` 对应的是同一个小场景。关系如下：

- `story-minimal.structured-script.yaml`：人工可维护的结构化剧本
- `story-minimal.casting-plan.yaml`：每个角色已经选好一个 `ready` 音色后的结果
- `story-minimal.script-runtime.json`：`build_tts_requests.py` 先做的一层规范化中间结果
- `story-minimal.tts-requests.json`：真正可 replay、可继续进 `synthesize_tts_requests.py` 的请求清单

这组示例里故意全部使用 official ready 音色，目的是让你更容易看清：

- 一个最小 `casting-plan` 至少要提供哪些字段
- `instruction / input_text / voice_id` 在 `tts-requests.json` 里最终长什么样
- `script-runtime` 和 `tts-requests` 的分工分别是什么

它会读取：

- 结构化剧本
- 同目录同名的 `*.casting-plan.yaml`

它会生成：

- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.script-runtime.json`
- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.tts-requests.json`

同时在 `tts-requests.json` 里写入建议整本输出路径：

- `source.output_path`

这个建议路径的扩展名，会跟 `common_request.response_format` 保持一致。

### 默认模型与附加参数

默认模型：

- `stepaudio-2.5-tts`

可透传的整本级参数：

- `--volume`
- `--tone-map`
- `--pronunciation-map-file`

它们会进入：

- `common_request.extra_body`

## `tts-requests.json` 的核心字段

这份文件是后续 replay 和局部修订的主入口。

顶层最重要的字段：

- `source`：输入文件和建议输出路径
- `common_request`：模型、采样率、返回格式、整本级 extra_body
- `segments[]`：每一段真正要送给 TTS 的请求

`segments[]` 里最关键的字段：

- `index`
- `speaker`
- `voice_id`
- `input_text`
- `instruction`
- `status`
- `audio_path`

## `instruction` 和 `input_text` 的分工

当前下游调用 StepAudio 2.5 TTS 时，默认约束如下：

- `input_text`：真正要发音的正文
- `instruction`：整段都成立的稳定控制语
- `input_text` 中前缀括号：句内或子句级的即时变化

推荐写法：

```text
instruction:
情绪克制，语速中速偏慢，压迫感轻微上扬

input_text:
（先压着火气）你终于回来了？（忽然失望）算了，我早该想到会这样。
```

当前实现限制：

- `input_text` 长度建议不超过 1000 字符
- `instruction` 长度建议不超过 200 字符
- 不支持 `voice_label`

## 第二步：合成分段音频

```bash
python3 scripts/synthesize_tts_requests.py --input /绝对路径/<base>.tts-requests.json
```

默认行为：

- 调用 `POST /v1/audio/speech`
- 把每段音频写入 `<base>.segments/`
- 回写 `segments[].status / audio_path / duration_ms`

默认输出目录：

```text
~/.openclaw/workspace/runs/audiobook/<slug>/<base>.segments/
```

### replay 行为

已成功且本地音频仍存在的段落，默认会跳过，不重复合成。

常用参数：

- 只合成几段：`--segments 1,3-5`
- 只重跑失败段：`--only-failed`
- 强制覆盖成功段：`--force`
- 仅预览不真正调用：`--dry-run`

### instruction 发送模式

默认：`--request-mode auto`

默认行为：

- 优先把 `instruction` 作为独立字段发送
- 如果接口明确报 `instruction is not supported`，再回退为把控制语并入 `input_text`

## 第三步：导出整本或试听片段

导出整本：

```bash
python3 scripts/finalize_audiobook.py --input /绝对路径/<base>.tts-requests.json
```

默认整本输出：

```text
~/.openclaw/workspace/runs/audiobook/<slug>/<base>.audiobook.<response_format>
```

导出局部试听：

```bash
python3 scripts/finalize_audiobook.py --input /绝对路径/<base>.tts-requests.json --segments 1,3-5
```

默认试听输出：

```text
~/.openclaw/workspace/runs/audiobook/<slug>/<base>.preview-1_3-5.<response_format>
```

导出时会：

- 校验选中段落都已成功合成
- 用 `ffmpeg` 拼接 `<base>.segments/` 里的音频
- 回写 `tts-requests.json -> latest_export`
- 如果是整本导出，再回写 `final_output`

## 程序化读取建议

如果你要让程序接管下游链路，建议这样读取：

1. 跑 `build_tts_requests.py`，拿 stdout JSON 里的 `output_path`
2. 跑 `synthesize_tts_requests.py`，检查返回的 `updated_segments`
3. 跑 `finalize_audiobook.py`，读取返回的 `output_path`
4. 再读取 `<base>.artifacts.json` 获取完整文件清单

这样比自己根据文件名规则拼路径更稳。

## 哪些情况会阻塞下游

`build_tts_requests.py` 会在下面这些情况直接报错：

- `casting-plan` 缺少 role
- 某个角色没有 `selected_voice_id`
- 某个角色 `selected_status != ready`
- 某个 clone 角色仍然停留在待付费状态

这属于故意设计：宁可早失败，也不要让下游默默生成一份半残的请求清单。
