# ConvoAI Quickstart

Onboarding flow for `quickstart` and `integration` modes (no proven working baseline yet).
Classify the mode in [README.md](README.md) first. For `advanced-feature` / `debugging` / `ops-hardening`, use [advanced.md](advanced.md).

## Sequence

Follow this exact user-visible order — do not skip ahead:

1. Product intro in plain language
2. Technical-path confirmation
3. Project-readiness checkpoint
4. Provider confirmation (default providers / custom providers / pipeline ID)
5. Sample-platform selection (only when the user chooses pipeline ID and platform is still unknown)
6. Detailed provider checklist (only if customization is needed and pipeline ID is not being reused)

## Product Intro

Use the product description from [README.md](README.md) (the architecture diagram and bullet points at the top) to give the user a brief plain-language intro to what ConvoAI is before asking any setup questions. Keep it short — orientation, not a deep dive. Then move to step 2.

## Language

Detect from the user's most recent message: Chinese → ZH prompts, otherwise → EN prompts. Stay consistent.

## Interaction Rules

- One decision group per turn — do not combine technical-path, credential, and provider in the same message
- Skip anything the user already answered
- Infer obvious context (e.g. user names Android → don't re-ask platform)
- If the user already named the platform, carry it forward into the pipeline path and do not ask the platform question again
- Do not propose project structures or framework names before the technical path is accepted
- Before mentioning ASR/LLM/TTS/provider, give a plain-language intro to what ConvoAI does
- Explain `App ID` and `App Certificate` in plain language before asking if the user has them
- If the user names an unsupported provider, resolve that blocker immediately
- Native platforms (iOS/Android/Windows/macOS): skip backend and token-server questions

## Defaults

| Field | Default | Notes |
|-------|---------|-------|
| Platform | `Web` | Skip for native platforms |
| Backend | `Python` | Skip entirely for native platforms |
| LLM | `aliyun` | |
| TTS | `bytedance` | |
| ASR | `fengming` | |
| ASR language | `zh-CN` | Use `en-US` for clearly English scenarios |

## Supported Providers

| Stage | Supported values |
|-------|-----------------|
| LLM | `aliyun`, `bytedance`, `deepseek`, `tencent` |
| TTS | `bytedance`, `microsoft`, `minimax`, `cosyvoice`, `tencent`, `stepfun` |
| ASR | `fengming`, `tencent`, `microsoft`, `xfyun`, `xfyun_bigmodel`, `xfyun_dialect` |

First-success baseline: `aliyun` + `bytedance` + `fengming`

If a named provider is outside the list (e.g. `openai`, `azure openai`, `kimi`, `google`), it is not supported by the ConvoAI platform — not just this quickstart path. Tell the user clearly that ConvoAI currently only supports the vendors listed above, and ask them to pick a supported alternative.

## State Machine

The quickstart is a blocking state machine. Each state must be resolved before advancing. While in any unresolved state, the ONLY allowed action is to send the corresponding prompt and wait for the user's reply.

| State | Allowed | Forbidden | Next prompt | Advance when |
|-------|---------|-----------|-------------|--------------|
| `intro` | Send product intro from README.md | Everything else | Product intro text | Intro delivered |
| `tech_path` | Ask technical-path prompt | Clone, code, sample inspection, framework names | Compact technical-path prompt | User picks A or B |
| `unsupported_provider` | Ask unsupported-provider prompt | Clone, code, sample inspection | Compact unsupported-provider prompt | User picks supported alternative (skip if no unsupported provider named) |
| `project_readiness` | Ask credential prompt | Clone, code, sample inspection, framework names | Compact credential prompt | User confirms ready or gets guidance |
| `providers` | Ask default-provider prompt or full checklist | Clone, code, sample inspection | Compact default-provider prompt or full checklist | User picks A/B/C. A → default providers resolved; B → continue with full checklist; C → `pipeline_platform` if platform is unknown, otherwise pipeline path resolved |
| `pipeline_platform` | Ask a platform-only follow-up built from the Detailed Provider Checklist rules | Clone, code, sample inspection, provider questions | Platform-only checklist using the existing Platform field format | User resolves the platform using the same checklist style as the Detailed Provider Checklist, then continue the pipeline-specific flow |
| `complete` | Emit structured spec, proceed to After Collection | — | — | — |

### Pre-action self-check

Before every tool call or message, verify:
1. What is the current state?
2. Is the intended action in the "Allowed" column for that state?
3. If not → do not perform it. Send the "Next prompt" instead.

### Failure branches

- If sample clone fails later (after `complete`) → report the blocker and wait for user choice. Do NOT silently fall back to `minimal-custom`.
- If network / permission is denied → report and wait. Do NOT improvise an alternative path.
- If the user's reply does not resolve the current gate → ask a narrow repair follow-up for the unresolved field only.

### Examples

Bad: route to quickstart → immediately clone the sample repo → ask provider questions later
Bad: route to quickstart → propose a Next.js + FastAPI project structure → then ask about credentials
Bad: user says "build a Web app" → first reply includes implementation plan or sample repo details
Good: user says "build a Web app" → first reply is product intro + technical-path prompt, nothing else
Good: route to quickstart → product intro → technical-path prompt → wait → unsupported-provider prompt only if needed → credential prompt → wait → default-provider prompt with A/B/C → if the user picks C and platform is still unknown, ask the platform-only checklist; otherwise carry the known platform forward → wait → all resolved → now proceed to After Collection

## Prompt Templates

### Technical Path

**ZH:**
```text
我建议先按官方 Web quickstart 路径继续，这样最快：
A. 用默认技术路径（官方 Web sample）
B. 我想自定义技术栈
```

**EN:**
```text
I suggest starting with the official Web quickstart path:
A. Use the default technical path (official Web sample)
B. I want a custom stack
```

Native variant: replace "Web" with the target platform name.

### Unsupported Provider

**ZH:**
```text
声网 ConvoAI 目前不支持 [provider]。
当前支持的 [stage] 厂商：[supported list]

A. 改用支持的默认厂商
B. 先看完整支持列表
```

**EN:**
```text
ConvoAI does not currently support [provider].
Supported [stage] vendors: [supported list]

A. Switch to the supported default
B. Show me the full supported list
```

### Credentials

**ZH:**
```text
继续前先确认三个前置条件：
- App ID：声网项目标识
- App Certificate：quickstart 用 RTC Token，需要这个
- ConvoAI 开通：项目需要先开通 ConvoAI 服务

A. 都准备好了
B. 还没有，告诉我去哪看
```

**EN:**
```text
Three prerequisites before we continue:
- App ID: your Shengwang project identifier
- App Certificate: needed for RTC Token auth
- ConvoAI activation: must be enabled for your project

A. All ready
B. Not yet — tell me where to find them
```

### Default Provider

**ZH:**
```text
默认三段式组合是：
- LLM：阿里云通义（需要 dashscope API key）
- TTS：火山引擎（需要 token + app_id）
- ASR：声网凤鸣（内置，无需额外 key）

A. 我有这些 key，按默认组合继续
B. 我没有 / 我要换其他厂商
C. 使用声网 Pipeline ID（需先在声网 Studio 完成三段式配置）
   Studio: https://console-conversationai.shengwang.cn/product/ConversationAI/studio
```

**EN:**
```text
The default provider combination is:
- LLM: Alibaba Cloud / Qwen (needs dashscope API key)
- TTS: Volcengine / ByteDance (needs token + app_id)
- ASR: Shengwang Fengming (built-in, no extra key needed)

A. I have these keys — continue with defaults
B. I don't have them / I want different providers
C. Use Shengwang Pipeline ID (configure the three-stage parameters in Shengwang Studio)
   Studio: https://console-conversationai.shengwang.cn/product/ConversationAI/studio
```

If the user picks `C`, do NOT ask the provider checklist. Continue with the pipeline path and resolve platform only if it is still unknown.

## Detailed Provider Checklist

Use only when the user asks to customize. Combine unresolved fields into one message.

Format rules:
- Number only visible unresolved fields starting from `1`
- Show supported options inline per field
- Mark defaultable fields as optional
- Accept sparse replies like `2B 4A`; omitted optional fields get defaults
- If user picks "Other", ask a narrow follow-up for that field only
- If the pipeline-ID path still needs platform, reuse this same checklist style but ask only for the unresolved `Platform` field

Provider options per field:

| Field | Options |
|-------|---------|
| Platform | Web, iOS, Android, Windows, macOS, Electron, Other |
| Backend | Python, Go, Java, Node.js, Other (skip for native) |
| LLM | aliyun, bytedance, deepseek, tencent |
| TTS | bytedance, microsoft, minimax, cosyvoice, tencent, stepfun |
| ASR | fengming, tencent, microsoft, xfyun, xfyun_bigmodel, xfyun_dialect |
| ASR language | zh-CN, en-US, Other |

## Output: Structured Spec

After all fields are resolved, normalize into this spec immediately — no extra confirmation turn needed.

```yaml
use_case: [text]
primary: ConvoAI
supporting: [RTC SDK | RTC SDK + RTM | RTC SDK + Cloud Recording | none]
platform: [Web | iOS | Android | Windows | macOS | Electron | other]
implementation: [sample-aligned | minimal-custom]
backend: [Python | Go | Java | Node.js | other | not needed]
project_readiness:
  app_id: [ready | missing | unknown]
  app_certificate: [ready | missing | unknown]
  convoai_activation: [ready | missing | unknown]
pipeline:
  existing_pipeline_id: [yes | no | unknown]
providers:
  asr: [fengming | tencent | microsoft | xfyun | xfyun_bigmodel | xfyun_dialect]
  asr_language: [zh-CN | en-US | other]
  llm: [aliyun | bytedance | deepseek | tencent]
  tts: [bytedance | minimax | tencent | microsoft | cosyvoice | stepfun]
```

## After Collection

- Use [pipeline-integration.md](pipeline-integration.md) when the user already has a pipeline ID and selected a sample platform
- Follow architecture rules in [README.md](README.md)
- Use [sample-repos.md](sample-repos.md) for sample inspection and clone
- Use [generation-rules.md](generation-rules.md) for code generation constraints
- Use [providers.md](providers.md) for vendor-specific required params when generating provider-based `/join` payloads
- Use `convoai-restapi/index.mdx` only for missing low-level API details

### Backend not covered by sample repo

| Backend | Official quickstart doc |
|---------|------------------------|
| Go | `docs://default/convoai/restful/get-started/quick-start-go` |
| Java | `docs://default/convoai/restful/get-started/quick-start-java` |

Use sample repo for frontend/architecture, official doc for backend details.
