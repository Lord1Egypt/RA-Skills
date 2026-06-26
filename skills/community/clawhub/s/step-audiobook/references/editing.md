# Audiobook Editing Guide

语言切换：当前为中文｜[English companion](./editing.en.md)

这份文档回答两件事：

1. 想改某个结果时，应该改哪个文件
2. 改完后，应该重跑哪一步

## 阅读导航 / Reading Guide

- 想看总入口与全局约定：回到 `../SKILL.md`
- 想看完整执行顺序：读 `./workflows.md`
- 想先理解音色库结构：读 `./voice-library.md`
- 想看下游 TTS 合成链路：读 `./synthesis.md`

如果你是第一次人工介入修改中间产物，推荐阅读顺序是：

1. `../SKILL.md`
2. `./workflows.md`
3. 当前这份 `./editing.md`
4. 遇到音色问题再回看 `./voice-library.md`

## 先看哪份文件

### 想改 clone 音色的真实描述

编辑：

- `~/.openclaw/workspace/audiobook-library/voice-reviews.yaml`
- 路径：`clones.<asset_id>.manual`

改完后执行：

```bash
python3 scripts/sync_voice_library.py --library ~/.openclaw/workspace/audiobook-library/voice-library.yaml --asset-id <asset_id> --refresh-profiles-only
```

### 想快速查看还有哪些 clone 音色没人工确认

执行：

```bash
python3 scripts/list_pending_reviews.py --library ~/.openclaw/workspace/audiobook-library/voice-library.yaml --pretty
```

如果你想把已经确认和未确认的都列出来：

```bash
python3 scripts/list_pending_reviews.py --library ~/.openclaw/workspace/audiobook-library/voice-library.yaml --all --pretty
```

### 想看模型本轮对某条参考音频的分析原文

查看：

- `~/.openclaw/workspace/audiobook-library/.audiobook/voice-analysis/<asset_id>.json`
- 或 `voice-reviews.yaml -> clones.<asset_id>.model_analysis`

这类文件通常用于排查，不建议手工改。

### 想看当前真正生效的 clone 画像

查看：

- `~/.openclaw/workspace/audiobook-library/.audiobook/effective-voice-library.yaml`

如果这里和你的预期不一致，优先回去改 `voice-reviews.yaml -> manual`。

### 想看后续选角实际读取的统一音色入口

查看：

- `~/.openclaw/workspace/audiobook-library/.audiobook/voice-candidate-pool.yaml`

或：

```bash
python3 scripts/list_voice_candidates.py --library ~/.openclaw/workspace/audiobook-library/voice-library.yaml --pretty
```

### 想改角色最终选中的音色

编辑：

- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.casting-review.yaml`
- 路径：`roles.<role_id>.manual`

改完后执行：

```bash
python3 scripts/recommend_casting.py --library ~/.openclaw/workspace/audiobook-library/voice-library.yaml --input /绝对路径/structured-script.yaml --refresh-only
```

### 想决定某个 clone 是否值得真正付费复刻

编辑：

- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.clone-review.yaml`
- 路径：`items.<asset_id>.manual.decision`

允许值：

- `confirm_clone`
- `skip`
- `pending`

改完后执行：

```bash
python3 scripts/recommend_casting.py --library ~/.openclaw/workspace/audiobook-library/voice-library.yaml --input /绝对路径/structured-script.yaml --refresh-only
```

### 想改故事内容 / speaker / 场景提示

编辑：

- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.structured-script.yaml`

改完后执行：

```bash
python3 scripts/build_tts_requests.py --input /绝对路径/structured-script.yaml
```

### 想改某一段真正送到 TTS 的文本或 instruction

编辑：

- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.tts-requests.json`

常见字段：

- `segments[].input_text`
- `segments[].instruction`
- `segments[].extra_body`
- `common_request.extra_body`

改完后执行：

```bash
python3 scripts/synthesize_tts_requests.py --input /绝对路径/<base>.tts-requests.json
```

如果只想重放部分段落：

```bash
python3 scripts/synthesize_tts_requests.py --input /绝对路径/<base>.tts-requests.json --segments 1,3-5
```

### 想试听已完成的部分，而不是整本导出

执行：

```bash
python3 scripts/finalize_audiobook.py --input /绝对路径/<base>.tts-requests.json --segments 1,3-5
```

## 不建议直接编辑的生成文件

这些文件建议只看不改：

- `~/.openclaw/workspace/audiobook-library/.audiobook/effective-voice-library.yaml`
- `~/.openclaw/workspace/audiobook-library/.audiobook/voice-candidate-pool.yaml`
- `~/.openclaw/workspace/audiobook-library/.audiobook/official-voices-cache.json`
- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.script-runtime.json`
- `~/.openclaw/workspace/runs/audiobook/<slug>/<base>.artifacts.json`

如果这些文件内容不对，应该回到上游人工入口去改，再重跑对应步骤。

## 重跑命令速查

### 改了音色人工描述

```bash
python3 scripts/sync_voice_library.py --library ~/.openclaw/workspace/audiobook-library/voice-library.yaml --asset-id <asset_id> --refresh-profiles-only
```

### 改了选角人工确认

```bash
python3 scripts/recommend_casting.py --library ~/.openclaw/workspace/audiobook-library/voice-library.yaml --input /绝对路径/structured-script.yaml --refresh-only
```

### 改了结构化剧本

```bash
python3 scripts/build_tts_requests.py --input /绝对路径/structured-script.yaml
```

### 改了 TTS 请求

```bash
python3 scripts/synthesize_tts_requests.py --input /绝对路径/<base>.tts-requests.json
```

### 只重跑失败段

```bash
python3 scripts/synthesize_tts_requests.py --input /绝对路径/<base>.tts-requests.json --only-failed
```

### 强制覆盖已成功段

```bash
python3 scripts/synthesize_tts_requests.py --input /绝对路径/<base>.tts-requests.json --force
```

### 重新导出整本

```bash
python3 scripts/finalize_audiobook.py --input /绝对路径/<base>.tts-requests.json --force
```

## 最后统一检查

每次人工修改后，建议检查：

```text
~/.openclaw/workspace/runs/audiobook/<slug>/<base>.artifacts.json
```

或：

```bash
python3 scripts/list_story_artifacts.py --manifest /绝对路径/<base>.artifacts.json --level review --pretty
```

这比手工记每一个中间产物路径更稳，也更适合程序对接。
