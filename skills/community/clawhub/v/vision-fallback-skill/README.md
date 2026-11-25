# vision-fallback

[![skills.sh](https://skills.sh/b/vst93/vision-fallback-skill)](https://skills.sh/vst93/vision-fallback-skill)
[![English](https://img.shields.io/badge/README-English-blue)](README.md)
[![中文](https://img.shields.io/badge/README-中文-red)](README.zh-CN.md)

Fallback multimodal vision skill for AI coding agents. Activates **only when
the primary vision model fails** to interpret an image (empty/unknown output,
low confidence, or user-reported failure), and performs structured image
understanding for UI screenshots, terminal outputs, mobile apps, and layout
reconstruction.

Calls an **OpenAI-compatible vision API** (`/chat/completions`) and returns
structured JSON (`summary`, `objects`, `text_detected`, `ui_structure`,
`inferred_elements`, `uncertainty_notes`).

## Providers

| `VISION_PROVIDER` | Backend | Default model | Key env var | Region |
|---|---|---|---|---|
| `ark` (default) | Volcengine Ark / doubao | `doubao-seed-2.0-lite` | `ARK_API_KEY` | Mainland China |
| `openai` | Any OpenAI-compatible API | `gpt-4o-mini` | `OPENAI_API_KEY` | Global |

`VISION_API_KEY` is a universal override that works for **any** provider. For
third-party endpoints (OpenRouter, Azure, vLLM, etc.), set `VISION_BASE_URL`
and `VISION_MODEL`.

> ⚠️ The default `ark` provider is hosted on Volcengine in **mainland China**.
> Users outside China may experience latency/reachability issues — switch to
> `VISION_PROVIDER=openai` for a globally available alternative.

---

## Install

### Generic (Claude Code, Cursor, Windsurf, Codex, …)

```bash
npx skills add vst93/vision-fallback-skill
```

> ℹ️ `npx skills add` installs into the harness's own skill directory (e.g.
> `~/.claude/skills/`). Other harnesses that scan different paths will **not**
> auto-discover it - see the harness-specific notes below.

### ClawHub

```bash
clawhub install @vst93/vision-fallback-skill
```

> The ClawHub slug is `vision-fallback-skill` (not `vision-fallback`).
> When publishing updates, use `clawhub sync` (not `clawhub skill publish`
> with a manual `--slug`), which auto-detects the correct slug and version.

### pi (earendil-works/pi-coding-agent)

pi does **not** scan `~/.claude/skills/`. Install into one of pi's discovery
locations instead:

```bash
# Option A: global skill dir (recommended)
git clone https://github.com/vst93/vision-fallback-skill \
  ~/.pi/agent/skills/vision-fallback

# Option B: link the repo you already have
ln -s /path/to/vision-fallback ~/.pi/agent/skills/vision-fallback
```

Or register the path in `~/.pi/agent/settings.json`:

```json
{
  "skills": ["/path/to/vision-fallback"]
}
```

For a project-scoped skill, place it under `.pi/skills/` (trusted project) or
`.agents/skills/` in the repo root instead.

### Verify

```bash
cd <skill-dir>
./scripts/check.sh
```

Checks shell deps, API key resolution, and endpoint reachability. Exits
non-zero with an actionable message if anything is missing.

Compatible with any agent harness that supports the
[Agent Skills standard](https://agentskills.io/specification).

---

## Configure

### Doubao (default)

```bash
export VISION_PROVIDER=ark
export ARK_API_KEY=xxxxxxxxxxxxxxxx
```

### OpenAI

```bash
export VISION_PROVIDER=openai
export OPENAI_API_KEY=sk-...
```

### Third-party OpenAI-compatible (OpenRouter, Azure, vLLM, …)

```bash
export VISION_PROVIDER=openai
export VISION_API_KEY=sk-...
export VISION_BASE_URL=https://your-provider.com/v1
export VISION_MODEL=your-vision-model
```

### Dotenv file

Instead of env vars, store keys in `~/.env_vars`:

```bash
# Provider config (all optional, env vars take precedence)
VISION_PROVIDER=openai
VISION_BASE_URL=https://your-provider.com/v1
VISION_MODEL=your-vision-model

# API key (one of the following)
VISION_API_KEY=xxxxxxxxxxxxxxxx
# or provider-specific:
# ARK_API_KEY=xxxxxxxxxxxxxxxx
# OPENAI_API_KEY=sk-...
```

See [`references/configuration.md`](references/configuration.md) for the full
key resolution order.

---

## Usage

The agent loads this skill automatically when the primary vision model fails.
To trigger manually:

```
/skill:vision-fallback
```

Core call:

```bash
./scripts/call-api.sh "$IMAGE" "$OCR_TEXT" "$FAILURE_REASON" "$PRIMARY_OUTPUT"
```

| Arg | Required | Description |
|-----|----------|-------------|
| `IMAGE` | Yes | Local file path, `http(s)://` URL, or `data:` URL |
| `OCR_TEXT` | No | OCR text extracted from the image |
| `FAILURE_REASON` | No | Why the primary model failed |
| `PRIMARY_OUTPUT` | No | The primary model's (insufficient) output |

---

## Structure

```
vision-fallback/
├── SKILL.md                      # Always loaded: trigger + workflow
├── scripts/
│   ├── check.sh                  # Preflight: deps + key + endpoint
│   ├── resolve-config.sh         # Provider/key/endpoint/model resolution
│   └── call-api.sh               # Image -> data URL + payload + curl POST
├── references/
│   ├── configuration.md          # Provider config, key resolution order
│   ├── api-reference.md          # Endpoint, headers, body schema
│   ├── output-format.md          # Response JSON schema
│   └── constraints.md            # Retry / escalation rules
└── assets/
    └── payload-template.json     # Request body template (jq-rendered)
```

## Constraints

- Only triggered when primary vision fails.
- Only one fallback call per image (no retry loop).
- If output is still insufficient → escalate by setting `VISION_MODEL` to a
  stronger model or switching `VISION_PROVIDER`. See
  [`references/constraints.md`](references/constraints.md).

## License

[MIT](LICENSE)
