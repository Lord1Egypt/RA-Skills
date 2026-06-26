# ConvoAI Provider Reference

Required `params` fields for each ASR / LLM / TTS vendor in the `/join` request body.
Source of truth: `agent-server-sdk` (Python package `shengwang_agent`).

> For optional fields and advanced config, fetch the vendor-specific docs or inspect the SDK source.

## LLM

All LLM vendors share the same param structure. The `vendor` field changes compatibility behavior.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `url` | string | yes | OpenAI-compatible endpoint URL |
| `api_key` | string | recommended | Required in production |
| `model` | string | no | Goes into `params.model` |
| `vendor` | string | no | `aliyun` / `bytedance` / `deepseek` / `tencent` / `custom` |

Common vendor URLs:

| Vendor | Default URL | Default model |
|--------|------------|---------------|
| `aliyun` | `https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions` | `qwen-plus` |
| `bytedance` | `https://ark.cn-beijing.volces.com/api/v3/chat/completions` | (user's deployed model endpoint ID) |
| `deepseek` | `https://api.deepseek.com/v1/chat/completions` | `deepseek-chat` |
| `tencent` | `https://api.lkeap.cloud.tencent.com/v1/chat/completions` | `deepseek-v3` |

Env vars needed: `LLM_API_KEY` (+ vendor-specific endpoint ID for bytedance).

## TTS

Each TTS vendor has different required params.

### bytedance (Volcengine TTS)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `token` | string | yes | Volcengine access token |
| `app_id` | string | yes | Volcengine app ID |
| `voice_type` | string | yes | e.g. `BV700_streaming` |
| `cluster` | string | no | e.g. `volcano_tts` |
| `speed_ratio` | float | no | |
| `volume_ratio` | float | no | |
| `pitch_ratio` | float | no | |

Env vars: `TTS_BYTEDANCE_TOKEN`, `TTS_BYTEDANCE_APP_ID`

### microsoft (Azure TTS)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `key` | string | yes | Azure subscription key |
| `region` | string | yes | e.g. `chinaeast2` |
| `voice_name` | string | yes | e.g. `zh-CN-YunxiNeural` |
| `speed` | float | no | 0.5–2.0 |
| `volume` | float | no | 0–100 |
| `sample_rate` | int | no | |

Env vars: `TTS_MICROSOFT_KEY`, `TTS_MICROSOFT_REGION`

### minimax

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `key` | string | yes | MiniMax API key |
| `model` | string | yes | e.g. `speech-01-turbo` |
| `voice_setting` | object | yes | `{voice_id, speed, vol, pitch, emotion}` |
| `group_id` | string | no | MiniMax group ID |
| `audio_setting` | object | no | `{sample_rate}` |

Env vars: `TTS_MINIMAX_KEY`, `TTS_MINIMAX_GROUP_ID`

### cosyvoice (Alibaba CosyVoice)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `api_key` | string | yes | CosyVoice API key |
| `model` | string | yes | e.g. `cosyvoice-v1` |
| `voice` | string | yes | e.g. `longxiaochun` |
| `sample_rate` | int | no | |

Env vars: `TTS_COSYVOICE_API_KEY`

### tencent

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `app_id` | string | yes | Tencent app ID |
| `secret_id` | string | yes | Tencent secret ID |
| `secret_key` | string | yes | Tencent secret key |
| `voice_type` | int | yes | Voice type ID, e.g. `601005` |
| `volume` | int | no | |
| `speed` | int | no | |

Env vars: `TTS_TENCENT_APP_ID`, `TTS_TENCENT_SECRET_ID`, `TTS_TENCENT_SECRET_KEY`

### stepfun

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `api_key` | string | yes | StepFun API key |
| `model` | string | yes | e.g. `step-tts-mini` |
| `voice_id` | string | yes | Voice ID |

Env vars: `TTS_STEPFUN_API_KEY`

### bytedance_duplex (Volcengine Duplex Streaming TTS)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `app_id` | string | yes | Volcengine app ID |
| `token` | string | yes | Volcengine token |
| `speaker` | string | yes | Speaker ID |

Env vars: `TTS_BYTEDANCE_TOKEN`, `TTS_BYTEDANCE_APP_ID`

## ASR

### fengming (Shengwang built-in)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `language` | string | no | Default `zh-CN`. Options: `zh-CN`, `en-US` |

No additional env vars needed — built-in service.

### tencent

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `key` | string | yes | Tencent secret key |
| `app_id` | string | yes | Tencent app ID |
| `secret` | string | yes | Tencent secret |
| `engine_model_type` | string | no | e.g. `16k_zh` |

Env vars: `ASR_TENCENT_KEY`, `ASR_TENCENT_APP_ID`, `ASR_TENCENT_SECRET`

### microsoft

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `key` | string | yes | Azure subscription key |
| `region` | string | yes | e.g. `chinaeast2` |
| `language` | string | no | Default `zh-CN` |
| `phrase_list` | string[] | no | Hotword list |

Env vars: `ASR_MICROSOFT_KEY`, `ASR_MICROSOFT_REGION`

### xfyun (iFlytek traditional)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `api_key` | string | yes | |
| `app_id` | string | yes | |
| `api_secret` | string | yes | |
| `language` | string | no | Default `zh_cn` |

Env vars: `ASR_XFYUN_API_KEY`, `ASR_XFYUN_APP_ID`, `ASR_XFYUN_API_SECRET`

### xfyun_bigmodel (iFlytek BigModel)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `api_key` | string | yes | |
| `app_id` | string | yes | |
| `api_secret` | string | yes | |
| `language_name` | string | no | Default `cn` |
| `language` | string | no | Default `mix` |

Env vars: same as `xfyun`

### xfyun_dialect (iFlytek Dialect)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `app_id` | string | yes | |
| `access_key_id` | string | yes | |
| `access_key_secret` | string | yes | |
| `language` | string | no | Default `zh-CN` |

Env vars: `ASR_XFYUN_APP_ID`, `ASR_XFYUN_ACCESS_KEY_ID`, `ASR_XFYUN_ACCESS_KEY_SECRET`

## Default Baseline

The quickstart default combination (`aliyun` + `bytedance` + `fengming`) requires:

| Stage | Env vars needed |
|-------|----------------|
| LLM (aliyun) | `LLM_API_KEY` |
| TTS (bytedance) | `TTS_BYTEDANCE_TOKEN`, `TTS_BYTEDANCE_APP_ID` |
| ASR (fengming) | none (built-in) |
