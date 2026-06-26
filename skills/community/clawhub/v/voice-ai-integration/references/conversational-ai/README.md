# Shengwang Conversational AI Engine (ConvoAI)

Real-time AI voice agent. User speaks into an RTC channel, agent responds via ASR → LLM → TTS pipeline.

```
User Device ── audio ──► RTC Channel ──► ConvoAI Agent (ASR → LLM → TTS)
User Device ◄── audio ── RTC Channel ◄── ConvoAI Agent
```

- Agent is server-side only — managed via REST API, no client SDK
- Client prefers `agora-agent-client-toolkit` when it fits; otherwise RTC SDK directly
- `POST /join` makes the agent join the same RTC channel

## Routing: Classify the Request

The key question: does the user have a **working ConvoAI baseline**?
- Working baseline = ConvoAI code that can run, or user explicitly says they have a working project
- Only RTC code, or sample repo checked out but never proven ConvoAI → **not** a working baseline

| Mode | When | Route to |
|------|------|----------|
| `quickstart` | Starting from scratch, first demo, no working baseline yet | [quickstart.md](quickstart.md) |
| `integration` | Has an app/repo, but ConvoAI path not yet proven end-to-end | [quickstart.md](quickstart.md) |
| `advanced-feature` | Working baseline confirmed, wants incremental capability | [advanced.md](advanced.md) |
| `debugging` | Error codes, Agent FAILED, broken behavior, logs | [advanced.md](advanced.md) |
| `ops-hardening` | Production auth, scaling, retries, quota, monitoring | [advanced.md](advanced.md) |

### Detection hints

- Quickstart signals: "从零开始", "最小 demo", "第一次接 ConvoAI", "按官方 sample 来"
- Integration signals: existing RTC app adding ConvoAI, sample-aligned into existing codebase
- Advanced signals: add MCP/tools, history, interrupt, template variables, switch provider on working flow
- Debug signals: HTTP 400/403/409/422/503, Agent FAILED, "why is this not working"
- Ops signals: auth strategy, quota, retry policy, monitoring, cost

### Routing rules

- Classify internally and proceed — do not output a classification message to the user
- If ambiguous, default to `quickstart` (safer path)
- `quickstart` and `integration` go through the full quickstart flow
- `advanced-feature` / `debugging` / `ops-hardening` skip the full quickstart
- `advanced-feature` and `debugging` may still trigger a partial preflight for the exact part being changed
- Do not force users with a working baseline back through quickstart
- Do not skip quickstart for users still blocked on foundational prerequisites

### Flow map

```text
README.md (classify mode)
  ├─ quickstart / integration → quickstart.md
  │    ├─ technical path → project readiness → provider confirmation
  │    └─ sample-repos.md → code generation
  └─ advanced / debugging / ops → advanced.md
       ├─ common-errors.md
       └─ convoai-restapi/ endpoint docs
```

## Architecture Defaults

1. Prefer official sample repo (`sample-aligned`) when it matches the user's stack
2. Server side: prefer `agent-server-sdk`
3. Client side: prefer `agora-agent-client-toolkit`; fall back to RTC SDK
4. Fetch Shengwang docs only after sample/SDK inspection leaves a gap
5. Use raw REST only for unsupported operations, debugging, or explicit REST-first requests

## Auth

- Quickstart requires: `App ID` + `App Certificate` + ConvoAI service activation
- Fixed auth path: RTC Token
- Details → [credentials-and-auth.md](../general/credentials-and-auth.md) · [token-server](../token-server/README.md)

## Reference Files

| File | Purpose |
|------|---------|
| [quickstart.md](quickstart.md) | Quickstart onboarding flow |
| [advanced.md](advanced.md) | Features / debugging / ops for existing projects |
| [providers.md](providers.md) | Required params per ASR / LLM / TTS vendor |
| [sample-repos.md](sample-repos.md) | Sample repo registry and alignment rules |
| [generation-rules.md](generation-rules.md) | Stable code generation constraints |
| [common-errors.md](common-errors.md) | Error diagnosis |
| [convoai-restapi/index.mdx](convoai-restapi/index.mdx) | REST endpoint index |
| [../doc-fetching.md](../doc-fetching.md) | Doc fetching guide |

## Docs Fallback

If fetch fails: https://doc.shengwang.cn/doc/convoai/restful/get-started/quick-start
