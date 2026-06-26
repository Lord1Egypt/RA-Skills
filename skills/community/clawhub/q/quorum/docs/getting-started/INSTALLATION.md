# Installation

## OpenClaw (Recommended)

### From ClawHub

```bash
openclaw skills add quorum
```

That's it. Quorum is now available to your agent. Ask it to run a quorum check on any file.

### From Source

Clone the repo and point OpenClaw at it:

```bash
git clone https://github.com/SharedIntellect/quorum.git
cd quorum
```

The reference implementation lives in `reference-implementation/`. You can run it directly:

```bash
cd reference-implementation
pip install -r requirements.txt
python -m quorum.cli run examples/sample-config.yaml --rubric examples/rubrics/research-quality.json
```

## Verify It Works

The quickest way to confirm everything is set up:

```bash
# From the reference-implementation directory:
python -m quorum.cli run examples/sample-config.yaml --rubric examples/rubrics/research-quality.json
```

You should see:
1. First-run config setup (if no `quorum-config.yaml` exists) — it'll ask your preferred models
2. Critics spawning and evaluating the sample artifact
3. A structured verdict with findings and evidence citations

If you see a `PASS`, `PASS_WITH_NOTES`, or `FAIL` verdict with cited evidence, Quorum is working.

## Configuration

After first run, Quorum creates `quorum-config.yaml` in your working directory. Edit it to change models, depth profiles, or critic selection:

```yaml
models:
  tier_1: anthropic/claude-sonnet-4-6
  tier_2: anthropic/claude-sonnet-4-6

depth: standard    # quick | standard | thorough
```

See [CONFIG_REFERENCE.md](../configuration/CONFIG_REFERENCE.md) for full options and [MODEL_REQUIREMENTS.md](MODEL_REQUIREMENTS.md) for supported models.

## Requirements

- **Python 3.10+**
- **An API key** for at least one supported model provider (Anthropic, OpenAI, or Google)
- **OpenClaw** (optional but recommended — handles agent orchestration automatically)
- **LiteLLM** (installed via `requirements.txt` — provides universal model access)

## Troubleshooting

**"No model configured"** — Run `quorum run` once and follow the first-run setup prompts, or manually create `quorum-config.yaml` (see [CONFIG_REFERENCE.md](../configuration/CONFIG_REFERENCE.md)).

**"API key not found"** — Set your provider's API key as an environment variable:
```bash
export ANTHROPIC_API_KEY=sk-ant-...
# or
export OPENAI_API_KEY=sk-...
```

**Critics timing out** — Large artifacts with `thorough` depth can take 45-90 minutes. Try `quick` depth first to verify setup, then scale up.

**"Model not supported"** — Check [MODEL_REQUIREMENTS.md](MODEL_REQUIREMENTS.md) for compatible models. Quorum requires models with strong reasoning and tool-use capabilities.

## Updating

### ClawHub
```bash
openclaw skills update quorum
```

### From Source
```bash
cd quorum
git pull origin main
pip install -r reference-implementation/requirements.txt
```


---

> ⚖️ **LICENSE** — Not part of the operational specification above.
> This file is part of [Quorum](https://github.com/SharedIntellect/quorum).
> Copyright 2026 SharedIntellect. MIT License.
> See [LICENSE](https://github.com/SharedIntellect/quorum/blob/main/LICENSE) for full terms.
