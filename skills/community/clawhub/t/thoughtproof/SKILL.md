---
name: thoughtproof
description: "Epistemic verification for AI agent outputs. Use ThoughtProof to verify AI reasoning, detect blind spots, and build consensus across multiple model families. Triggers: when an agent needs a second opinion, audit trail for decisions, or epistemic consensus. Works with any LLM backend (BYOK). Commands: tp verify, tp deep, tp list, tp show."
---

# ThoughtProof — Epistemic Verification Skill

Multi-agent verification protocol for AI decisions. Like a TÜV for AI reasoning.

## How It Works

ThoughtProof runs your question through multiple independent AI agents (different model families), then a critic layer identifies blind spots, and a synthesizer produces a consensus with confidence scores.

**Pipeline:** Normalize → Generate (3+ models) → Critique (adversarial) → Evaluate → Synthesize

## Prerequisites

- `pot-cli` installed: `npm install -g pot-cli`
- At least one API key (Anthropic, OpenAI, xAI, or Moonshot)
- More keys = more model diversity = better verification

## Quick Start

### Verify a claim or decision

```bash
tp verify "Should we use microservices or monolith for our MVP?"
```

### Chain context from previous verifications

```bash
tp verify --context last "What about scaling considerations?"
```

### Deep analysis with rotated roles

```bash
tp deep "Is this investment thesis sound?"
```

## Configuration

pot-cli reads config from `~/.potrc.json`:

```json
{
  "generators": [
    { "provider": "xai",       "model": "grok-4-1-fast" },
    { "provider": "moonshot",  "model": "kimi-k2.5" },
    { "provider": "anthropic", "model": "claude-sonnet-4-6" }
  ],
  "critic":      { "provider": "anthropic", "model": "claude-opus-4-6" },
  "synthesizer": { "provider": "anthropic", "model": "claude-opus-4-6" }
}
```

Show current config: `tp config`

### Model Diversity Requirement

ThoughtProof enforces ≥3 different model families for generators. This is core to the protocol — no single provider can verify itself.

## Output

Each verification produces an **Epistemic Block**:

- **Proposals** from each generator (independent reasoning)
- **Critique** identifying blind spots, contradictions, and risks
- **Synthesis** with consensus score, confidence level, and dissent
- **MDI** (Model Diversity Index) — measures independence of reasoning

Blocks are stored locally as JSON and can be reviewed with `tp list` / `tp show <n>`.

## Commands

| Command | Description |
|---------|-------------|
| `tp verify <question>` | Run full verification pipeline |
| `tp verify --context last` | Chain from previous block |
| `tp deep <question>` | Deep verify: multiple runs, rotated roles, meta-synthesis |
| `tp list` | Show block history |
| `tp show <n>` | Show a specific block |
| `tp config` | Show current configuration |

## Tiers

| Tier | Agents | Time | Best For |
|------|--------|------|----------|
| Light | 3 | ~30s | Quick sanity checks |
| Standard | 5-7 | ~3min | Business decisions |
| Deep | 7-12 | ~5min | High-stakes, regulatory |

## When to Use ThoughtProof

- **High-stakes decisions** — investment, legal, medical, compliance
- **Audit trail needed** — regulatory, governance, due diligence
- **Blind spot detection** — when you suspect a single model is biased
- **Cross-domain questions** — where no single model is expert

## When NOT to Use

- Simple factual lookups (Google it)
- Creative writing (subjective, no "correct" answer)
- Time-sensitive queries under 30 seconds
- Questions with trivially verifiable answers

## Architecture Note

ThoughtProof is BYOK (Bring Your Own Key). Your API keys, your data, your models. Nothing routes through ThoughtProof servers. The skill is MIT-licensed; the consensus protocol is BSL-licensed.

## References

- `references/block-format.md` — Epistemic Block JSON schema
- `references/consensus-protocol.md` — How consensus is calculated
