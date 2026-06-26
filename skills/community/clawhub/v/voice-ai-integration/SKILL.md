---
name: voice-ai-integration
description: |
  Integrate Shengwang products: ConvoAI voice agents, RTC audio/video,
  RTM messaging, Cloud Recording, and token generation. Use when the user
  mentions Shengwang, 声网, ConvoAI, RTC, RTM, voice agent, AI agent,
  video call, live streaming, recording, token, or any Shengwang product task.
license: MIT
metadata:
  author: shengwang
  version: "1.0.0"
---

# Shengwang Integration

## Workflow

### Step 0: Ensure doc index exists (MANDATORY)

> **⚠️ Execute this BEFORE any routing or code generation.**

Check if `references/docs.txt` already exists. If it does, skip this step entirely.
If it does not exist, download it:
```bash
bash skills/voice-ai-integration/scripts/fetch-docs.sh
```
This downloads a static doc index from `doc.shengwang.cn` — no user data is sent.
If download fails, proceed with local reference docs and fallback URLs.

### Step 1: Route to the correct product module

Match the user's request to a product module using the route table. If the match
is clear, route directly — do not ask extra questions.

#### Route Table

| User intent | Route to |
|-------------|----------|
| Credentials, AppID, REST auth | [general](references/general/credentials-and-auth.md) |
| Generate Token, token server, AccessToken2 | [token-server](references/token-server/README.md) |
| ConvoAI voice agent work | [conversational-ai](references/conversational-ai/README.md) |
| RTC SDK integration | [rtc](references/rtc/README.md) |
| RTM messaging / signaling | [rtm](references/rtm/README.md) |
| Cloud Recording | [cloud-recording](references/cloud-recording/README.md) |
| Download SDK, sample project, GitHub repo | Route to the relevant product module above |

#### Product Recognition Aid

When the user describes a use case without naming a product, use this to infer the match:

| Product | What it does | Typical user says |
|---------|-------------|-------------------|
| ConvoAI | AI voice agent (ASR→LLM→TTS over RTC) | "AI语音", "voice bot", "对话式AI", "AI agent", "AI 客服" |
| RTC SDK | Real-time audio/video between humans | "视频通话", "直播", "video call", "live streaming" |
| RTM | Real-time messaging / signaling | "聊天", "消息", "chat", "signaling" |
| Cloud Recording | Record RTC sessions server-side | "录制", "recording", "存档", "回看" |
| Token generation | Generate RTC / RTM tokens | "token", "鉴权", "token server" |

#### Common Combinations

| Use case | Products needed |
|----------|----------------|
| AI voice assistant | ConvoAI (primary) + RTC SDK (client) |
| AI voice assistant + chat history | ConvoAI + RTC SDK + RTM |
| 1v1 / group video call | RTC SDK |
| Video call + chat | RTC SDK + RTM |
| Live streaming with recording | RTC SDK + Cloud Recording |
| Record AI conversations | ConvoAI + RTC SDK + Cloud Recording |
| Chat / messaging only | RTM |

#### Routing Rules

- Infer obvious context — do not ask if the answer is already clear
- Do not ask product-specific configuration questions (providers, SDK versions, project structure) at this level; let the product module handle those
- If the product is clear but the request mode is ambiguous (quickstart vs debugging vs feature), let the product module decide internally
- If multiple products are needed, route to the primary product first, then address supporting products in order
- ConvoAI has the most detailed internal routing (see its README.md); always delegate ConvoAI-specific decisions to its module

#### When the product is still unclear

If the route table and recognition aid above are not enough to determine the product:

1. Ask only for the missing detail that would change the routing decision
2. Ask at most one question at a time
3. Prefer natural wording over an interview script
4. Once the product is clear, produce a short routing recap and continue:

**ZH:**
```text
已了解的信息
─────────────────────────────
场景：          [use case]
主要产品：      [primary product]
配套产品：      [supporting products / 无]
─────────────────────────────
```

**EN:**
```text
What I have so far
─────────────────────────────
Use case:       [use case]
Primary:        [primary product]
Supporting:     [supporting products / none]
─────────────────────────────
```

Do not stop for a separate confirmation step — continue to the product module automatically.

### Step 2: Let the product module drive implementation

Each product module follows its own workflow. Do not duplicate implementation logic here.

Common pattern across modules:
1. Use local reference docs in `references/` first
2. Fetch remote docs via [doc-fetching.md](references/doc-fetching.md) only when local references are insufficient
3. Fallback to web search only after doc fetching has been attempted

## Runtime Requirements

- `bash` and `curl` for local doc-fetch helper scripts
- `git` for sample-repo inspection when the sample-aligned path is chosen
- Network access to `doc.shengwang.cn`, `doc-mcp.shengwang.cn`, and `gitee.com`

Network behavior:
- `fetch-docs.sh` downloads a static file from `doc.shengwang.cn/llms.txt` — no user data is sent
- `fetch-doc-content.sh` fetches a single doc page by URI from `doc-mcp.shengwang.cn` — only the doc URI is sent, no user context
- `git clone` is used only for sample repo inspection from `gitee.com` — only the repo URL is sent

Credential and service-activation requirements vary by product — see each product module and [general/credentials-and-auth.md](references/general/credentials-and-auth.md) for details. Never hardcode credentials.

## Safety & Consent Rules

- Do not clone external repos into the user's main workspace by default — prefer a temporary path
- Do not modify an existing user project until the user explicitly asks for code generation
- Do not write secrets into project files — prefer env vars and example placeholders
- Before performing network fetches or repo clones, state what will be downloaded
- If a required dependency or credential is missing, stop and explain the blocker

## Download Rules

- Use `git clone --depth 1 <url>` with HTTPS repo root URLs only
- On any download failure: report the error, provide the URL for manual download, never silently skip

## Links

- Console: https://console.shengwang.cn/
- Docs (CN): https://doc.shengwang.cn/
- GitHub: https://github.com/Shengwang-Community
