> **Update (v3.28.0):** OpenClaw now writes the Codex OAuth token to `OPENAI_CODEX_API_KEY` in `~/.openclaw/.env`. Sage Router reads that env var **first**, then falls back to the auth-profiles file at runtime. The `openclaw-gateway` bridge is only used when no token is present at all. See [Use Sage Router with OpenClaw](integrations/openclaw.md) for the precedence list.

# OpenAI Codex OAuth Token Passthrough

## Architecture Overview

OpenAI Codex via OpenClaw uses **OAuth authentication**, not traditional API keys. This document explains how to correctly configure `openai-codex` provider routing.

## The Problem

When configuring `openai-codex` as a provider, requests fail with:
```
FailoverError: Unknown model: openai-codex/gpt-5.5
```

This happens because `openai-codex` is not a normal OpenAI API-key provider. It requires OAuth token passthrough from OpenClaw's auth profiles.

## Correct Configuration

### 1. Auth Profile Setup

OpenClaw stores OAuth tokens in:
```
~/.openclaw/agents/main/agent/auth-profiles.json
```

Profile shape:
```json
{
  "openai-codex:your@email.com": {
    "provider": "openai-codex",
    "type": "oauth",
    "access": "<oauth_access_token>",
    "expires": <unix_timestamp_ms>
  }
}
```

### 2. Provider Configuration in openclaw.json

Add `openai-codex` as a provider with `api: "openai-codex-responses"`:

```json
{
  "models": {
    "providers": {
      "ollama": { ... },
      "sage-router": { ... },
      "openai-codex": {
        "baseUrl": "http://127.0.0.1:8790",
        "api": "openai-codex-responses",
        "models": [
          { "id": "gpt-5.5", "name": "gpt-5.5", "reasoning": true, "input": ["text"] },
          { "id": "gpt-5.4", "name": "gpt-5.4", "reasoning": true, "input": ["text"] }
        ]
      }
    }
  }
}
```

### 3. Fallback Configuration

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "sage-router/frontier",
        "fallbacks": ["ollama/glm-5:cloud", "openai-codex/gpt-5.5"]
      }
    }
  }
}
```

## How Token Passthrough Works

When Sage Router receives a request for `openai-codex`:

1. **No static API key** - The provider has no `apiKey` configured
2. **Runtime token discovery** - Router reads from auth profile at runtime:
   ```python
   if provider.name == "openai-codex" and not provider.api_key:
       profile = find_auth_profile(provider="openai-codex", type="oauth")
       if profile and profile["expires"] > now_ms:
           api_key = profile["access"]
   ```
3. **Bearer token injection** - Token is injected as `Authorization: Bearer <token>`
4. **Request routing** - Request goes to OpenAI Codex backend via OpenClaw gateway

## Sage Router Virtual Provider

In `router.py`, openai-codex is defined as a gateway provider:

```python
GATEWAY_PROVIDER_PROFILES = {
    'openai-codex': (
        'openclaw-gateway',
        DEFAULT_OPENAI_CODEX_MODELS,
        {'reasoning': True, 'contextWindow': 256000, 'maxTokens': 128000, 'input': ['text']}
    ),
    # ... other providers
}

DEFAULT_OPENAI_CODEX_MODELS = [
    'gpt-5.5', 'gpt-5.4', 'gpt-5.4-pro', 'gpt-5.4-mini',
    'gpt-5.3-codex', 'gpt-5.3-codex-spark', 'gpt-5.2-codex',
    'gpt-5.1-codex-max', 'gpt-5.1-codex-mini', 'gpt-5.1'
]
```

## Key Insights

1. **OAuth-backed at auth layer** - openai-codex uses OAuth tokens, not `sk-*` API keys
2. **Gateway routing** - Requests go through OpenClaw gateway (`openclaw-gateway` or `openai-codex-responses` API type)
3. **Runtime token validation** - Tokens are validated against `expires` before use
4. **No secrets in config** - Never copy OAuth tokens into openclaw.json; read from auth profiles at runtime

## Request Flow

```
Client Request
    ↓
Sage Router (localhost:8790)
    ↓
Model Selection: openai-codex/gpt-5.5
    ↓
Auth Profile Lookup: ~/.openclaw/agents/main/agent/auth-profiles.json
    ↓
Token Validation: expires > now_ms ?
    ↓
Bearer Token Injection: Authorization: Bearer <access>
    ↓
OpenClaw Gateway → OpenAI Codex Backend
    ↓
Response
```

## Troubleshooting

### "Unknown model: openai-codex/gpt-5.5"

**Cause**: Provider not configured or wrong API type

**Fix**: Add provider with `api: "openai-codex-responses"` and models list

### "Agent couldn't generate a response"

**Cause**: Token expired or missing auth profile

**Fix**:
1. Check auth profile exists: `cat ~/.openclaw/agents/main/agent/auth-profiles.json | jq '.profiles | keys'`
2. Re-authenticate via OpenClaw if token expired

### Token Expiration

OAuth tokens have limited lifetime. OpenClaw handles refresh automatically when:
- User re-authenticates via `openclaw auth openai-codex`
- Browser-based OAuth flow refreshes token

## Implementation Gotcha

Do NOT store OAuth tokens in openclaw.json config. Read them at runtime:

```python
# Correct pattern
if provider == "openai-codex" and not api_key:
    profile = find_auth_profile(provider="openai-codex", type="oauth")
    if profile and profile["expires"] > now_ms:
        api_key = profile["access"]  # Runtime injection only
```

Treat it as an OAuth bearer token for the Codex backend, not an OpenAI project key.

## Related Files

- `~/.openclaw/openclaw.json` - Provider and model configuration
- `~/.openclaw/agents/main/agent/auth-profiles.json` - OAuth token storage
- `sage-router/router.py` - Provider routing logic (GATEWAY_PROVIDER_PROFILES)
- `sage-router/README.md` - Full provider documentation

## References

- Sage Router README: OpenClaw Gateway section
- GATEWAY_PROVIDER_PROFILES in router.py defines all gateway-backed providers
- Local-strict mode excludes openai-codex (cloud provider) but allows Darkbloom (decentralized)