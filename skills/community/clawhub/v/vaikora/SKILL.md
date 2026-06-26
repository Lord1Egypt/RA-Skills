---
name: vaikora-security
description: Route OpenClaw LLM calls through Vaikora for real-time AI agent security monitoring. Every action your agent takes gets scored for risk, anomaly-flagged, and pushed as a security signal to SentinelOne, CrowdStrike, or AWS Security Hub, without changing how your agent works.
version: 1.0.1
metadata:
  openclaw:
    requires:
      env:
        - VAIKORA_API_KEY
        - VAIKORA_AGENT_ID
        - LLM_PROVIDER_API_KEY
    primaryEnv: VAIKORA_API_KEY
    emoji: "🛡️"
    homepage: https://vaikora.com
---

# Vaikora Security

Vaikora is a reverse proxy for AI agents. It sits between OpenClaw and your LLM provider (OpenAI, Anthropic, Gemini, Bedrock, etc.) and inspects every request and response before it reaches the model.

What it does:
- Scores each agent action for risk on a 0 to 100 scale
- Detects anomalies with ML trained on adversarial prompt examples
- Blocks prompt injection, jailbreaks, and PII exfiltration attempts
- Scans LLM responses for toxicity and data leakage
- Emits behavioral signals that downstream connectors (SentinelOne, CrowdStrike, AWS Security Hub) can ingest

Your agent code does not change. You change the base URL and add two headers.

## What Vaikora receives

Because Vaikora sits in the request path, it sees:
- The full prompt and message history your agent sends
- The full response returned by the upstream LLM
- Your upstream LLM provider key, which Vaikora forwards to the provider on your behalf

If any of that is a problem for your use case, read the data handling section below before you route production traffic through it. A test key and isolated agent account are the safest way to evaluate.

## Setup

You need a Vaikora account and API key. Get one at [vaikora.com](https://vaikora.com). The free tier covers 20 req/min and 7-day audit retention, no card required.

Set three environment variables:

```bash
# Vaikora gateway credential (identifies you to Vaikora)
export VAIKORA_API_KEY=vk_live_...

# Vaikora agent identifier (scopes the audit trail)
export VAIKORA_AGENT_ID=your-agent-id

# Your upstream LLM provider key (Vaikora forwards this to the provider)
export LLM_PROVIDER_API_KEY=sk-...
```

`LLM_PROVIDER_API_KEY` is whatever key the provider issues you. OpenAI's `sk-...`, Anthropic's `sk-ant-...`, a Google API key, etc. Vaikora does not store it beyond the request lifetime, but it does see it in cleartext.

## How routing works

Vaikora exposes a drop-in OpenAI-compatible endpoint at `https://api.vaikora.com/v1`. The completions path is `/v1/chat/completions`, same as OpenAI.

In your OpenClaw config, change the base URL and set two headers:

```yaml
# Before
llm:
  provider: openai
  base_url: https://api.openai.com/v1
  headers:
    Authorization: "Bearer ${LLM_PROVIDER_API_KEY}"

# After
llm:
  provider: openai
  base_url: https://api.vaikora.com/v1
  headers:
    x-api-key: "${VAIKORA_API_KEY}"
    Authorization: "Bearer ${LLM_PROVIDER_API_KEY}"
    x-vaikora-agent: "${VAIKORA_AGENT_ID}"
```

Header roles:
- `x-api-key` authenticates your request to Vaikora
- `Authorization: Bearer` carries your upstream provider key. Vaikora forwards this to OpenAI, Anthropic, or whichever provider your chosen model maps to.
- `x-vaikora-agent` tags the action in Vaikora's audit log

This mirrors the dual-header pattern documented in the Data443 LLM Gateway QA handbook. Works with any provider OpenClaw supports: OpenAI, Anthropic, Google, Azure, Bedrock, Mistral, Groq, Ollama.

## Security connectors

Vaikora captures every action. To push high-risk signals into your SIEM or EDR, install a connector from AWS Marketplace. Each is free:

| Platform | What it does |
|----------|-------------|
| SentinelOne | Maps high-risk agent actions to IOCs via Threat Intelligence API |
| CrowdStrike Falcon | Pushes risky actions as Custom IOCs. Critical = prevent mode. High = detect mode. |
| AWS Security Hub | Sends ASFF findings for high-severity and anomalous actions |

Search "Vaikora" in [AWS Marketplace](https://aws.amazon.com/marketplace). Connectors run on your infrastructure (Lambda or Logic Apps) and poll Vaikora's API on a schedule.

## What gets monitored

Every action is scored across four dimensions:

| Dimension | What it checks |
|-----------|----------------|
| Risk Score | Composite 0 to 100 based on content, context, and intent |
| Anomaly | ML deviation from this agent's baseline behavior |
| Policy | Allow, block, or audit decision against configured rules |
| Threat | Confirmed malicious activity flag with 0 to 1 confidence score |

Actions with risk score at 75 or above, an anomaly flag, or a confirmed threat get forwarded to your security connector as a finding.

## Verifying routing is live

After the config change, run a test prompt through your agent, then query Vaikora's management API to confirm the action was logged:

```bash
curl -H "x-api-key: ${VAIKORA_API_KEY}" \
  "https://api.vaikora.com/api/v1/actions?agent_id=${VAIKORA_AGENT_ID}&per_page=5"
```

Note the two paths:
- `/v1/...` is the OpenAI-compatible gateway (where your agent sends traffic)
- `/api/v1/...` is Vaikora's management API for reading audit data

You should see the action with a risk score and threat assessment.

## Policy presets

Activate a preset in your Vaikora config:

| Preset | Use case |
|--------|----------|
| `standard` | Default, balanced security |
| `strict` | High-sensitivity environments |
| `permissive` | Dev and test, minimal blocking |
| `hipaa` | PHI detection, medical data protection |
| `pci-dss` | Credit card and financial data protection |
| `gdpr` | EU PII categories, Right to Erasure support |

```yaml
# vaikora.yaml
policy: hipaa
```

## Data handling notes

Because Vaikora is in the request path, treat it like any other vendor with access to your prompts and provider credentials:

- Use a dedicated upstream provider key with spend limits while evaluating
- Do not route PHI, PCI, or regulated data until you have reviewed Vaikora's retention and access controls
- Rotate your provider key after testing
- Use `vk_test_...` keys for local development

Vaikora's docs cover retention and access at [vaikora.com/docs](https://vaikora.com/docs).

## Performance

- Gateway latency: P50 = 8ms, P95 = 22ms
- Block decisions are early-exit, around 18ms
- Published threat detection accuracy: 99.9%, false positive rate under 0.1%

## Links

- [Vaikora docs](https://vaikora.com/docs)
- [AWS Marketplace, Security Hub connector](https://aws.amazon.com/marketplace/pp/prodview-dotgh5y3ox6rq)
- [AWS Marketplace, SentinelOne connector](https://aws.amazon.com/marketplace/pp/prodview-tzxzdoajtk3bu)
- [AWS Marketplace, CrowdStrike connector](https://aws.amazon.com/marketplace/pp/prodview-cs7idbycte7fm)
- [Data443 Risk Mitigation](https://data443.com)
