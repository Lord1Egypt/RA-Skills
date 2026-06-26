# Token Plan 团队版 vs Standard API Key

> Sources:
> - https://platform.qianwenai.com/pricing/token-plan
> - https://platform.qianwenai.com/home/billing/subscription/token-plan
> Updated: 2026-05-01

## Two Key Types

千问云 has two mutually exclusive authentication systems. Mixing them produces hard-to-diagnose errors.

| Dimension | Standard Key (Pay-as-you-go) | Token Plan 团队版 |
|-----------|------------------------------|-------------------|
| Key format | `sk-xxxxx` | `sk-sp-xxxxx` |
| OpenAI-compatible URL | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| Anthropic-compatible URL | N/A | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| Native DashScope URL | `https://dashscope.aliyuncs.com/api/v1` | **Not supported on text endpoints**; image generation uses dedicated `https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation` |
| Auth header | `Authorization: Bearer <key>` | `Authorization: Bearer <key>` (NOT `x-api-key`) |
| Supported text models | Full catalog (100+) | **4 text LLMs** (see below) |
| Supported image models | Full catalog | **4 image models** via Skill/extension only (see below) |
| Video / TTS / ASR / Embedding | Available | **Not supported** |
| Usage scope | Any API call (scripts, apps, tools) | **Interactive AI tools only** (Cursor, Claude Code, Qwen Code, OpenClaw, OpenCode, Codex, Kilo Code/CLI, Hermes Agent, etc.) |
| Billing | Per-token consumption (CNY) | **Credits**: monthly seat allowance + shared usage packages |
| Quota exhaustion | Continues (pay more or use prepaid balance) | **Hard fail — service paused** until next cycle or shared package purchased |

> [!WARNING]
> **Forbidden uses for `sk-sp-` Token Plan keys**: automation scripts, application backends, batch jobs,
> API testing tools (Postman/Insomnia), workflow platforms (Dify, n8n, Coze). Violations may trigger
> subscription suspension or API Key revocation.

## Supported Models

### Text Models (4 total)

| Model            | Context Window | OpenAI-compat | Anthropic-compat | Notes                          |
|------------------|---------------:|:-------------:|:----------------:|--------------------------------|
| `qwen3.6-plus`   |             1M | ✅            | ✅               | Flagship; multimodal text+image input; thinking mode (`thinkingFormat: qwen`); built-in tools (web search, code interpreter, web fetch, image search) via Responses API |
| `glm-5`          |           198K | ✅            | ✅               | Thinking mode supported        |
| `MiniMax-M2.5`   |           192K | ✅            | ✅               | budgetTokens + output ≤ 32768  |
| `deepseek-v3.2`  |           128K | ✅            | ❌ **OpenAI only** | Use `compatible-mode/v1` only  |

### Image Generation Models (4 total)

> [!IMPORTANT]
> Image generation models **cannot** be invoked through the text Base URL. They use a dedicated
> multimodal-generation endpoint and must be wired up via each tool's Skill / Slash Command / Agent
> mechanism (NOT through the standard model selector).

| Model                | Notes                                                              |
|----------------------|--------------------------------------------------------------------|
| `qwen-image-2.0`     | Default; general-purpose; strong Chinese text rendering            |
| `qwen-image-2.0-pro` | Higher quality, slightly slower                                    |
| `wan2.7-image`       | Multi-style; returns 4 images by default                           |
| `wan2.7-image-pro`   | Supports 4K (additional sizes: 2048×2048, 1440×2560, 2560×1440)    |

Available sizes: `1024*1024` (default), `720*1280`, `1280*720`. `wan2.7-image-pro` adds 4K options above.

Endpoint: `POST https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

## Credits Billing Mechanism

- **Unit**: Credits. Single-call cost depends on model, token usage, thinking mode, and tool calls.
- **Tiers**: 标准坐席 (¥198/seat/month, 25,000 Credits) · 高级坐席 (¥698/seat/month, 100,000 Credits) · 尊享坐席 (¥1,398/seat/month, 250,000 Credits).
- **Shared usage package**: ¥5,000 per package, 625,000 Credits, 1-month validity, expires unused.
- **Deduction order**: seat monthly quota → shared package (nearest-expiry first) → service paused.
- **Reset**: seat quotas reset monthly; unused credits do not roll over.

Example (qwen3.6-plus single request): 8,349 input + 40,794 cached + 573 output ≈ 3.18 Credits.

## Key Type × Endpoint — Expected Behavior

| Key Type | Base URL | Result |
|----------|----------|--------|
| `sk-` | `dashscope.aliyuncs.com/...` | OK |
| `sk-` | `token-plan.cn-beijing.maas.aliyuncs.com/...` | **`Incorrect API key provided`** — standard key rejected on Token Plan endpoint |
| `sk-sp-` | `dashscope.aliyuncs.com/...` | **`InvalidApiKey: Invalid API-key provided`** — Token Plan key rejected on standard endpoint |
| `sk-sp-` | `token-plan.cn-beijing.maas.aliyuncs.com/...` (via tool) | OK |
| `sk-sp-` | `token-plan.cn-beijing.maas.aliyuncs.com/...` (via raw script/curl outside an AI tool) | **Policy violation** — may trigger suspension |

## Common Errors

| Error                                            | Cause                                                                              | Resolution                                                                                |
|--------------------------------------------------|------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| `InvalidApiKey: No API-key provided`             | Key not configured, or tool used `x-api-key` header                                | Set key; switch to `Authorization: Bearer`                                                |
| `InvalidApiKey: Invalid API-key provided`        | Standard `sk-` key used, subscription expired, key copied with whitespace          | Use `sk-sp-` Token Plan key; verify subscription status; reset key in console             |
| `model 'xxx' not found or not supported`         | Model name typo / wrong case; model not supported on chosen protocol               | Match model ID exactly; `deepseek-v3.2` only via OpenAI-compat                            |
| `invalid access token or token expired`          | Wrong Base URL (e.g. used another plan's endpoint)                                 | Use Token Plan Base URL listed above                                                      |
| `Incorrect API key provided`                     | Used `dashscope.aliyuncs.com` Base URL with Token Plan key                         | Switch to `token-plan.cn-beijing.maas.aliyuncs.com` endpoint                              |
| `Range of input length should be [1, xxx]`       | Input + history exceeds context window                                             | Start a new session, compact context, or switch to a larger-context model                 |
| `Connection error`                               | Base URL typo or network issue                                                     | Verify Base URL spelling and connectivity                                                 |
| `API rate limit reached`                         | Routed to shared API quota due to mis-config; or seat / shared package exhausted   | Verify provider config; check Token Plan console for usage; reset key as last resort      |

## Impact on QianWen-AI/qianwen-ai Scripts

All execution scripts (`qianwen-text`, `qianwen-vision`, `qianwen-image-generation`, `qianwen-video-generation`,
`qianwen-audio-tts`) call DashScope directly via `urllib.request` and are **not** recognized as AI tools.
They detect `sk-sp-` keys and print a warning to stderr.

| Skill                       | API Type      | Works with `sk-sp-` Token Plan key? | Reason                                                                              |
|-----------------------------|---------------|:-----------------------------------:|-------------------------------------------------------------------------------------|
| qianwen-text                | OpenAI-compat |                  ❌                 | Standard endpoint rejects `sk-sp-`; scripts are not AI tools                        |
| qianwen-vision              | OpenAI-compat |                  ❌                 | Same; vision models not in Token Plan list                                          |
| qianwen-image-generation    | Native        |                  ❌                 | Standard `dashscope.aliyuncs.com` not accepted by Token Plan; image models on Token Plan need separate endpoint via tool Skill mechanism |
| qianwen-video-generation    | Native        |                  ❌                 | Video models unavailable in Token Plan                                              |
| qianwen-audio-tts           | Native        |                  ❌                 | TTS models unavailable in Token Plan                                                |

**Action**: Set a standard `sk-` key in `DASHSCOPE_API_KEY` when using these execution skills. The
Token Plan `sk-sp-` key is for the AI tool itself (Cursor, Claude Code, etc.), not for backend scripts.

## Cost Risk Scenarios

1. **`sk-sp-` key in scripts**: 401/`Incorrect API key provided`, no charges, but confusing.
2. **`sk-` key when user expects Token Plan coverage**: Calls succeed but incur pay-as-you-go charges.
   Cannot detect programmatically — documentation must clarify.
3. **`QWEN_BASE_URL` set to Token Plan endpoint with `sk-` key**: Authentication fails.
4. **Token Plan Credits exhausted**: Hard fail, no fallback to pay-as-you-go.

## Console & Billing

| Resource                  | URL                                                                |
|---------------------------|--------------------------------------------------------------------|
| Token Plan Subscription   | https://platform.qianwenai.com/home/billing/subscription/token-plan                |
| Token Plan Pricing        | https://platform.qianwenai.com/docs/token-plan/overview#%E5%A5%97%E9%A4%90%E4%B8%8E%E5%AE%9A%E4%BB%B7                  |
| Pay-as-you-go Billing     | https://platform.qianwenai.com/home/billing/pay-as-you-go      |
| Usage Analytics (PAYG)    | https://platform.qianwenai.com/home/analytics                  |

> [!NOTE]
> **Usage queries**: Token Plan seat & shared-package Credits balance are currently only viewable in
> the [Token Plan console](https://platform.qianwenai.com/home/billing/subscription/token-plan) (Subscription page →
> Token Plan tab). The `qianwen` CLI does not yet support `sk-sp-` Token Plan team-edition keys; CLI
> commands (`qianwen usage summary`, etc.) only work for standard `sk-` keys.

## Coexistence

Both key types can be held simultaneously by the same user:
- `sk-sp-` Token Plan key → configured in the AI tool (Cursor, Claude Code, OpenClaw, ...)
- `sk-` standard key → set in `DASHSCOPE_API_KEY` for QianWen-AI/qianwen-ai execution scripts

These are independent; configuring one does not affect the other.
