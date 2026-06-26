# Shengwang Credentials & Authentication

Cross-product knowledge shared by all Shengwang products.

## Credentials

| Credential | Where to find | Used for |
|------------|--------------|---------|
| `SHENGWANG_APP_ID` | Console → Project Overview | All API calls and SDK init |
| `SHENGWANG_CUSTOMER_KEY` | Console → Settings → RESTful API | REST API Basic Auth username |
| `SHENGWANG_CUSTOMER_SECRET` | Console → Settings → RESTful API | REST API Basic Auth password |
| `SHENGWANG_APP_CERTIFICATE` | Console → Project Overview | Token generation (only if enabled) |

Console: https://console.shengwang.cn/

### Environment Variables

```bash
SHENGWANG_APP_ID=your_app_id
SHENGWANG_CUSTOMER_KEY=your_customer_key
SHENGWANG_CUSTOMER_SECRET=your_customer_secret
SHENGWANG_APP_CERTIFICATE=your_app_certificate   # only if App Certificate enabled
```

- ALWAYS read from env vars — never hardcode
- NEVER put secrets in client-side code
- NEVER commit `.env` with real values

### Service Activation

Some products require extra activation in Console beyond having credentials:

| Product | Extra requirement |
|---------|------------------|
| ConvoAI | Enable ConvoAI service (403 if not done) |
| Cloud Recording | Enable Cloud Recording service |
| RTC / RTM | No extra activation needed |

## REST API Authentication

Shengwang REST APIs support two authentication methods (choose one).

> **An RTC Token serves two purposes in Shengwang:**
> 1. **REST API auth** — placed in the HTTP `Authorization` header to authenticate API calls (e.g. ConvoAI `/join`). This is Option 1 below.
> 2. **Channel join auth** — placed in the SDK's `joinChannel` call or in a REST body field like `token` in `/join`, to let a client or agent enter an RTC channel.
>
> Both uses can share the same RTC Token. The difference is the layer: HTTP-level auth vs media-level auth.
> Token generation is the same for both — see [token-server](../token-server/README.md).

### Option 1: RTC Token

```
Authorization: agora token="007abcxxxxxxx123"
```

```bash
curl -H "Authorization: agora token=\"$RTC_TOKEN\"" \
     -H "Content-Type: application/json" \
     https://api.agora.io/...
```

For how to generate the token value, see [token-server](../token-server/README.md).

### Option 2: Basic Auth

```
Authorization: Basic base64("{SHENGWANG_CUSTOMER_KEY}:{SHENGWANG_CUSTOMER_SECRET}")
```

```bash
AUTH=$(echo -n "$SHENGWANG_CUSTOMER_KEY:$SHENGWANG_CUSTOMER_SECRET" | base64)
curl -H "Authorization: Basic $AUTH" \
     -H "Content-Type: application/json" \
     https://api.agora.io/...
```

> Not all products support Token auth. Cloud Recording only supports Basic Auth. Check each product module's docs.

## Docs

Fetch docs using the doc fetching script (see [doc-fetching.md](../doc-fetching.md)):

| Topic | Command |
|-------|---------|
| Token authentication overview | `bash skills/voice-ai-integration/scripts/fetch-doc-content.sh "docs://default/rtc/android/basic-features/token-authentication"` |

## Docs Fallback

If fetch fails: https://doc.shengwang.cn/doc/rtc/android/basic-features/token-authentication
