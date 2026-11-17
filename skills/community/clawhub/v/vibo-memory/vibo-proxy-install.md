# ViBo Proxy — Installation & Setup

A self-hostable privacy layer: encrypt secrets (AES-256-GCM) and mask them (`🔒[name]`) before prompts reach an LLM provider. OpenAI-compatible — works with DeepSeek, OpenAI, and any `base_url`-configurable agent.

**© 2026 ViBo by Viacheslav Bochkarev** · https://wwwvibo.com · hello@wwwvibo.com

## Requirements

- Docker (recommended) — or Python 3.11 + `pip install -r requirements.txt`
- An upstream LLM API key (e.g. DeepSeek, OpenAI)

## Install (Docker, one command)

```bash
UPSTREAM_API_KEY=<your-api-key> bash setup.sh
```

This builds and runs the proxy on **http://localhost:8017**. Data (encrypted secrets + audit) lives in `./data/`.

## Point your agent at the proxy

Change the agent's `base_url` to the proxy:

```yaml
base_url: http://localhost:8017/v1        # self-hosted (default — prompts stay on your machine)
# or:     https://wwwvibo.com/v1          # hosted — ⚠️ prompts + masked metadata transit an external
                                          # service (explicit opt-in trust boundary). Use self-hosted
                                          # for confidential work.
```

That's it — prompts now pass through the filter.

## Use

```bash
# 1. Register a secret (encrypted, ciphertext only) — LOCAL endpoint, nothing leaves the machine
curl -X POST http://localhost:8017/secrets \
  -H "Content-Type: application/json" \
  -d '{"name":"api_key","value":"sk-your-secret"}'

# 2. Chat through the proxy — the secret is masked as 🔒[api_key]
curl -X POST http://localhost:8017/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-chat","messages":[{"role":"user","content":"my key is sk-your-secret — what is it?"}]}'
# → response carries "vibo": {"secrets_blocked": 1, ...}

# 3. Reveal a secret (admin only)
curl -X POST http://localhost:8017/secrets/reveal \
  -H "Content-Type: application/json" -d '{"name":"api_key"}'
```

## Configuration (env)

| Var | Default | Meaning |
|---|---|---|
| `UPSTREAM_BASE_URL` | `https://api.deepseek.com/v1` | the LLM provider to proxy to |
| `UPSTREAM_API_KEY` | — | the upstream LLM key (required) |
| `PRIVACY_ADMIN_TOKEN` | empty → localhost-only | protect `/secrets` management |
| `VIBO_DATA_DIR` | `./data` | where the DB + key live |
| `PORT` | `8017` | listen port |

## Privacy notes

- Secrets are encrypted at rest (AES-256-GCM) and stored as ciphertext only.
- The audit log records *how many* secrets were blocked; the names are encrypted too.
- The rest of the prompt is forwarded to the upstream LLM as-is (it must read it to answer).
- For zero-knowledge (the proxy can't read secrets), use the client-side encryption variant.
