# Audiobook Voice Library

语言切换：当前为中文｜[English companion](./voice-library.en.md)

这份文档说明 `audiobook` 的音色库放在哪里、每个文件负责什么、用户参考音频怎样流转到后续选角与 TTS。

## 阅读导航 / Reading Guide

- 想看总入口与全局约定：回到 `../SKILL.md`
- 想看完整执行顺序：读 `./workflows.md`
- 想手工修改后重跑：读 `./editing.md`
- 想看角色如何基于音色库做选角：读 `./casting.md`

如果你是第一次维护音色库，推荐阅读顺序是：

1. `../SKILL.md`
2. 当前这份 `./voice-library.md`
3. `./workflows.md`
4. 需要人工修订时再进入 `./editing.md`

## 默认路径

```bash
WORKSPACE_ROOT=~/.openclaw/workspace
LIBRARY_ROOT=$WORKSPACE_ROOT/audiobook-library
VOICE_LIBRARY=$LIBRARY_ROOT/voice-library.yaml
```

如果团队需要自定义目录，不要改脚本常量，优先改 `voice-library.yaml -> paths`。这份文档下面展示的都是默认路径。

默认目录结构：

```text
audiobook-library/
  voice-library.yaml
  voice-reviews.yaml
  voices/
    inbox/
    references/
      <asset_id>/
        raw.<ext>
        reference.wav
  .audiobook/
    official-voices-cache.json
    voice-analysis/
      <asset_id>.json
    effective-voice-library.yaml
    voice-candidate-pool.yaml
    voice-registry.json
    voice-previews/
```

## 模板文件和示例文件的区别

skill 里有两套看起来相近、用途不同的文件：

1. `assets/voice-library.template.yaml` / `assets/voice-reviews.template.yaml`
   - 用来初始化你真正要运行的库文件
   - 注释更完整，适合第一次落地
2. `examples/voice-library.minimal.yaml` / `examples/voice-reviews.minimal.yaml`
   - 用来快速理解最小结构
   - 适合程序对字段、人工复制局部片段、做最小 mock
   - 不建议直接替代正式运行中的库文件

`examples/voice-library.minimal.yaml` 里演示了两种常见 clone 状态：

- 一个已经入库、等待人工确认是否值得付费 clone
- 一个只是预登记，还没真正 ingest 音频

`examples/voice-reviews.minimal.yaml` 里则演示了：

- 一个已经人工确认、`manual` 生效的条目
- 一个仍然待人工确认、只能先回退到 `archived_analysis` 的条目

## 每个文件的职责

### `voice-library.yaml`

位置：`~/.openclaw/workspace/audiobook-library/voice-library.yaml`

用途：音色库的主配置文件。

这里保存：

- 路径配置
- 官方音色同步状态
- clone 资产元信息
- `selected_for_clone`
- `source_file` / `raw_file`
- LLM 配置

这里不应该承载最终的人工音色画像正文。

### `voice-reviews.yaml`

位置：`~/.openclaw/workspace/audiobook-library/voice-reviews.yaml`

用途：用户人工确认 clone 音色的唯一入口。

如果你想在第一次 ingest 前先准备一份带注释的骨架，可以先复制：

```bash
cp ~/.openclaw/workspace/skills/audiobook/assets/voice-reviews.template.yaml \
   ~/.openclaw/workspace/audiobook-library/voice-reviews.yaml
```

如果你不手工初始化，也没关系；第一次执行 `sync_voice_library.py` 时，脚本会自动创建这份文件。

每个 clone 条目包含：

- `manual`：用户最终确认的描述、标签、适合场景、避免场景、稳定 instruction
- `model_analysis`：模型本轮分析归档
- `archived_analysis`：从模型结果提炼的候选画像
- `review`：当前是否还待确认

生效优先级：

```text
manual > archived_analysis > empty
```

快速查看哪些 clone 还处于待人工确认状态：

```bash
python3 scripts/list_pending_reviews.py --library "$VOICE_LIBRARY" --pretty
```

### `voices/inbox/`

位置：`~/.openclaw/workspace/audiobook-library/voices/inbox/`

用途：待处理投递区。

你可以把新音频先放这里，再执行：

```bash
python3 scripts/sync_voice_library.py --library "$VOICE_LIBRARY"
```

注意两点：

- 不带 `--input` 时，`sync_voice_library.py` 当前只会消费 `inbox/` 里排在最前面的 1 条音频
- 成功入库后，文件会被移动到 `voices/references/<asset_id>/raw.<ext>`，不会继续留在 inbox

如果你要一次性处理 `inbox/` 里的全部文件，建议执行：

```bash
python3 scripts/run_audiobook.py --library "$VOICE_LIBRARY" --process-inbox --downstream-mode off
```

### `voices/references/<asset_id>/`

用途：长期保留的参考音频资产目录。

里面通常有：

- `raw.<ext>`：原始上传音频
- `reference.wav`：标准化后的单声道 24k wav

这两份都应该长期保留，不建议在 clone 成功后自动删除。

### `.audiobook/voice-analysis/<asset_id>.json`

用途：单次音频分析的完整归档。

里面至少会保留：

- `raw_text`
- `raw_model_result`
- `structured_result`（如果做过二次结构化）
- `normalized_result`
- `analysis_pipeline`

这份文件适合排查模型分析问题；不建议直接作为后续选角入口。

### `.audiobook/effective-voice-library.yaml`

用途：程序生成的 clone 生效视图。

后续流程读取 clone 音色时，应优先读这里，而不是直接读 `voice-reviews.yaml`。

### `.audiobook/official-voices-cache.json`

用途：最近一次官方音色接口同步结果。

当前会保留：

- `official_description`
- `recommended_scenes`
- `selection_summary`
- `information_quality`

`display_name` 只用于展示，不应作为选角的主要依据。

### `.audiobook/voice-candidate-pool.yaml`

用途：官方音色 + clone 生效音色的统一音色候选池。

角色选角时，应该只读这份文件。

### `.audiobook/voice-registry.json`

用途：已完成付费 clone 的注册表。

这里会保存：

- `voice_id`
- `file_id`
- `preview_wav`
- `prepared_at`

## 用户参考音频的完整流转

```text
原始音频
-> voices/inbox/                或 --input /绝对路径/音频
-> voices/references/<asset_id>/raw.<ext>
-> voices/references/<asset_id>/reference.wav
-> step-audio-r1.1 分析
-> .audiobook/voice-analysis/<asset_id>.json
-> voice-reviews.yaml
   - manual
   - archived_analysis
-> .audiobook/effective-voice-library.yaml
-> .audiobook/voice-candidate-pool.yaml
-> recommend_casting.py
```

## r1.1 分析阶段现在怎么做

`sync_voice_library.py` 对用户参考音频会执行：

1. 标准化为 `reference.wav`
2. 调用 `step-audio-r1.1`
3. 要求模型只分析长期声线特征，不要转写台词
4. 如果首次返回更像转写文本，自动补一次更强的 `no transcript` 重试
5. 把结果写入 `voice-analysis/<asset_id>.json`
6. 生成 `archived_analysis`
7. 保留 `manual`，不自动覆盖用户已确认内容

关键原则：

- 证据不足就写 `unknown`
- 不因“年轻、温柔、甜美”等词硬推性别
- `manual` 永远优先于自动分析

## 官方音色是怎样进库的

官方音色不写回 `voice-library.yaml` 的正文区，而是走：

```text
Step official voices API
-> .audiobook/official-voices-cache.json
-> .audiobook/voice-candidate-pool.yaml
```

这样做的好处：

- 用户手工字段不会被官方接口覆盖
- 官方音色可以每次运行时刷新
- 角色选角只需要读统一音色候选池

## 付费 clone 的边界

当前只有 `clone_selected_voices.py` 会真正付费 clone。

此前的所有步骤都只是在做：

- 参考音频入库
- 声音画像分析
- 候选 clone 筛选
- 等待人工确认

推荐顺序：

```bash
python3 scripts/clone_selected_voices.py --library "$VOICE_LIBRARY" --dry-run
python3 scripts/clone_selected_voices.py --library "$VOICE_LIBRARY" --confirm-paid-action
```

但真正被 `clone_selected_voices.py` 读取的不是故事目录下的 `clone-review.yaml`，而是库级 `voice-library.yaml -> clones.<asset_id>.selected_for_clone`。

如果你的 clone 决策来自某本书的 `clone-review.yaml`，顺序应当是：

```bash
python3 scripts/recommend_casting.py --library "$VOICE_LIBRARY" --input /绝对路径/structured-script.yaml --refresh-only
python3 scripts/clone_selected_voices.py --library "$VOICE_LIBRARY" --dry-run
python3 scripts/clone_selected_voices.py --library "$VOICE_LIBRARY" --confirm-paid-action
```

第一步的作用，是把 `items.<asset_id>.manual.decision` 同步回库级 `selected_for_clone`。clone 成功后，`voice_id` 会进入 `voice-registry.json`，并同步回生效音色库与统一候选池。

## 推荐的人工编辑入口

只改这几个地方：

- 调整 clone 描述：`voice-reviews.yaml -> clones.<asset_id>.manual`
- 调整 clone 是否进入付费队列：`*.clone-review.yaml -> items.<asset_id>.manual.decision`
- 调整库级 clone 资产开关：`voice-library.yaml -> clones.<asset_id>.enabled / selected_for_clone`

不建议直接改：

- `.audiobook/effective-voice-library.yaml`
- `.audiobook/voice-candidate-pool.yaml`
- `.audiobook/official-voices-cache.json`
- `.audiobook/voice-analysis/<asset_id>.json`

如果你只是想先看“还有哪些条目没确认”，优先不要直接翻 YAML，先执行：

```bash
python3 scripts/list_pending_reviews.py --library "$VOICE_LIBRARY" --pretty
```
