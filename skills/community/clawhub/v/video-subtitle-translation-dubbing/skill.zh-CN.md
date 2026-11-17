# video-subtitle-translation-dubbing

[English](./skill.md) | [简体中文]

**OpenClaw 技能** —— 支持多语言视频字幕翻译与自动配音，并按需生成配音后的多音轨、多字幕轨视频。

- **Name**: `video-subtitle-translation-dubbing`
- **Version**: `0.1.4`
- **Entrypoint**: `translation_dubbing_skill.run`
- **Manifest**: [`manifest.yaml`](./manifest.yaml)

## 概述

该技能读取输入视频（支持外挂字幕或自动提取视频内嵌字幕轨），输出：

- 独立的翻译后目标语言字幕文件（UTF-8 SRT/VTT）
- 一段合成后的 `.mkv` 视频

调用方通过 `processing_mode` 参数选择两种处理模式之一：

| 处理模式 | TTS | 音轨 | 字幕轨 |
|---------|-----|------|--------|
| `subtitle_only` | 跳过 | 仅保留原音轨（默认） | 目标语言字幕轨（默认）+ 原语言字幕轨 |
| `subtitle_and_dubbing`（默认） | 合成目标语言配音 | 目标语言配音（默认）+ 原音轨 | 目标语言字幕轨（默认）+ 原语言字幕轨 |

## 快速开始

```python
from translation_dubbing_skill import parse_manifest, run

params = parse_manifest({
    "video_path": "/path/to/input.mp4",
    "subtitle_path": "/path/to/input.en.srt",   # 可选
    "source_language": "en",
    "target_language": "zh-CN",
    "processing_mode": "subtitle_and_dubbing",
    "translation_provider": "llm",
    "translation_endpoint": "https://api.example.com/v1/chat/completions",
    "translation_credential": "sk-...",
    "translation_config": {"model_name": "gpt-4o-mini"},
    "tts_provider": "edge",
    "tts_endpoint": "none",
    "tts_credential": "none",
})

result = await run(params)
print(result.output_video_path, result.output_subtitle_path)
```

## 输入

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `video_path` | path | 是 | 输入视频文件，扩展名必须在 `supported_video_formats` 内 |
| `subtitle_path` | path | 否 | 外挂字幕（`.srt` / `.vtt`）；缺失时从视频提取内嵌字幕轨 |
| `source_language` | string | 是 | 原始视频/字幕语言代码（默认 `en`） |
| `target_language` | string | 是 | 目标翻译/TTS语言代码（默认 `zh-CN`） |
| `processing_mode` | enum | 是 | `subtitle_only` \| `subtitle_and_dubbing`（默认） |
| `voice_id` | string | 否 | TTS 语音标识；`subtitle_only` 模式下忽略 |
| `translation_provider` | enum | 是 | `llm` \| `web` |
| `translation_endpoint` | string | 是 | 翻译提供方 HTTP 端点 |
| `translation_credential` | secret | 是 | 翻译凭证（日志/错误对象中会脱敏为 `***`） |
| `translation_config` | object | 否 | 翻译提供方自定义配置 |
| `translation_rate_limit` | object | 否 | 批量/文本量/并发自适应配置 |
| `tts_provider` | enum | 条件必填 | `llm` \| `web` \| `edge`；`subtitle_and_dubbing` 模式下必填 |
| `tts_endpoint` | string | 条件必填 | TTS 提供方 HTTP 端点 |
| `tts_credential` | secret | 条件必填 | TTS 凭证 |
| `tts_config` | object | 否 | TTS 提供方自定义配置 |
| `tts_rate_limit` | object | 否 | TTS 自适应调度配置 |

完整字段定义与默认值见 [`manifest.yaml`](./manifest.yaml)。

## 输出

| 字段 | 类型 | 说明 |
|------|------|------|
| `output_video_path` | path | 合成后的 `.mkv` 视频 |
| `output_subtitle_path` | path | 目标语言字幕文件（UTF-8 SRT/VTT，格式与输入一致） |

### 输出视频结构

**`subtitle_and_dubbing`** 模式：

```
streams:
  video:  video  (codec copy, 保持分辨率/帧率/编码)
  audio:  target (AAC, language=target, default=1, title="Target Dubbing")
          source (copy, language=source, default=0, title="Original Audio")
  subs:   target (SRT, language=target, default=1, title="Target Subtitle")
          source (SRT, language=source, default=0, title="Original Subtitle")
```

**`subtitle_only`** 模式：

```
streams:
  video:  video  (codec copy)
  audio:  source (copy, language=source, default=1)
  subs:   target (SRT, language=target, default=1)
          source (SRT, language=source, default=0)
```

## 进度事件

该技能通过 OpenClaw 运行时注入的进度回调逐阶段上报执行进度：

```
parsing → translating → [tts] → muxing → done
```

- `translating` 阶段携带 `completed / total`（已翻译条目数 / 总条目数），严格单调不减
- `tts` 阶段仅在 `subtitle_and_dubbing` 模式下出现，同样携带进度计数
- `done` 阶段在 `extra` 中返回 `output_video_path / output_subtitle_path`

## 可插拔提供方

内置提供方（通过 `@register` 在模块加载时自动注册）：

| kind | provider_type | 说明 |
|------|--------------|------|
| `translation` | `llm` | 调用大语言模型翻译端点；批量 JSON 数组往返 |
| `translation` | `web` | 调用第三方翻译 REST API |
| `tts` | `llm` | 调用大语言模型 TTS 端点（支持批量） |
| `tts` | `web` | 调用第三方 TTS REST API（单条） |
| `tts` | `edge` | 调用 Microsoft Edge Read-Aloud 内置免费 TTS 服务 |

新增提供方只需在 `translation_dubbing_skill.providers.{translation,tts}` 下实现协议并用 `@register(kind, provider_type)` 装饰即可，**调用方代码无需改动**。

## 自适应调度

翻译与 TTS 调用统一由 `AdaptiveScheduler` 驱动，三维自适应：

- **批量大小**（batch_size）：一次请求携带的条目数
- **单次请求文本量**（payload_size）：按字符数或估算 token 数衡量
- **并发度**（concurrency）：同时未完成的请求数

AIMD 策略：连续成功升档；命中 `429`（`RateLimitError`）乘性降档三维 + 退避等待（优先使用 `Retry-After`）；命中 `413` 或上下文窗口超长（`PayloadTooLargeError`）仅降 `payload_size` 并重新切分且不占用重试预算；`5xx`/超时（`TransientError`）退避重试但不降档。

默认参数见 `manifest.yaml` 的 `translation_rate_limit / tts_rate_limit.default`。

## 错误模型

所有错误都是 `SkillError` 的子类，携带 `stage / code / reason / context` 四元组。敏感键（`credential / api_key / authorization`）在 `to_dict()` 序列化时自动脱敏为 `***`。

## 环境依赖

- **Python** ≥ 3.11
- **ffmpeg** / **ffprobe**：必须在 `PATH` 中可用。用于字幕提取、音频变速/对齐、视频合成、元数据探测
- **httpx**：HTTP 客户端
- **pydub**：音频拼接与响度归一化
- **PyYAML**：解析 manifest

## 限制与边界

- 目标语音合成发音人可通过 `voice_id` 显式设置；若缺省则会根据目标语种代码自动进行默认高保真声线映射（Edge-TTS 支持 `en`, `zh`, `ja`, `es`, `fr`, `de`, `ko` 等常用语种）
- 输出视频固定为 Matroska（`.mkv`）容器
- 音频变速通过 ffmpeg `atempo` 滤镜链实现，单阶段范围 `[0.5, 2.0]`，链式组合支持任意正速率
- 对齐算法保证与输入视频时长误差 ≤ 100 ms
- `subtitle_only` 模式下调用方提供的 `tts_*` 字段与 `voice_id` 被**完全忽略**

## 许可与归属

见仓库根目录的 `LICENSE` 与 `pyproject.toml` 声明。
