# use-hln-api

`use-hln-api` is an agent skill for working with the Hyperliquid Names API & HyperEVM integration flows.

## Hyperliquid Names

Hyperliquid Names is a protocol for issuing & managing `.hl` names on HyperEVM. It supports:

- Forward resolution: name -> address
- Reverse resolution / primary names: address -> name
- Profile and data records
- Third-party minting flows via the HL Names API

## What This Skill Is For

This skill helps an agent:

- Resolve `.hl` names and reverse-resolve addresses
- Fetch profiles, records, expiry, images, and owner/list queries
- Interpret HL Names API validation and error behavior
- Assist with HyperEVM dApp integration and mint-pass preparation

## What’s In This Repo

- `skills/use-hln-api/`: canonical Claude-compatible skill source
- `SKILL.md`: generated root copy for Codex compatibility
- `references/`: generated root reference copies for Codex compatibility
- `agents/openai.yaml`: Codex/OpenAI skill metadata
- `.claude-plugin/plugin.json`: Claude plugin metadata
- `scripts/sync-codex-skill.sh`: checks for drift & syncs canonical Claude skill files into the Codex root layout only when needed

## Eval Suite

- `evals/use-hln-api.lvl1.yaml`: `Lvl 1` core regression suite
- `evals/use-hln-api.lvl2.yaml`: `Lvl 2` harder suite for stronger baselines and HLN-specific workflow/boundary checks
- `runner/run.sh`: eval runner with `with_skill` vs `without_skill` A/B mode
- `runner/report.sh`: Markdown report generator from `benchmark.json`
- `results/`: local eval artifacts; only `results/.gitkeep` is intended for Git

### Eval Setup

Copy the env template and fill in the keys you actually plan to use:

```bash
cp .env.example .env
```

The runner auto-loads `./.env` if present. For live evals, `HLN_API_KEY` is optional because the runner falls back to the built-in public agent key. Set it only if you want to override that default.

- `HLN_API_KEY` or the built-in fallback key
- the provider key for the selected `--model`
- the provider key for the selected `--judge`

Defaults:

- answer model: `openai/gpt-5.4-nano`
- judge model: `openai/gpt-5.4-nano`
- eval file: `evals/use-hln-api.lvl1.yaml`

### Eval Usage

Run the default `Lvl 1` suite:

```bash
./runner/run.sh
```

Run the harder `Lvl 2` suite:

```bash
./runner/run.sh --eval-file evals/use-hln-api.lvl2.yaml
```

Run one eval only:

```bash
./runner/run.sh --eval-file evals/use-hln-api.lvl2.yaml --eval lvl2-live-mintpass-expiry-hard-mode
```

Run with Venice models:

```bash
./runner/run.sh --eval-file evals/use-hln-api.lvl2.yaml --model venice/claude-sonnet-4-6 --judge venice/claude-sonnet-4-6
```

The runner writes each run under `results/iteration-<timestamp>/` and also emits:

- `benchmark.json`
- `RESULTS.md`

## Install / Use

### Codex CLI

Codex uses skills from `~/.codex/skills/<skill-name>`.

```bash
mkdir -p ~/.codex/skills
cp -R . ~/.codex/skills/use-hln-api
```

Restart Codex after installing.

For maintainers: Codex reads the root `SKILL.md` and `references/`, which are generated from `skills/use-hln-api/` via `scripts/sync-codex-skill.sh`.

### Claude Code CLI

This repo now includes the minimal Claude plugin wrapper:

- `.claude-plugin/plugin.json`
- `skills/use-hln-api/`

Use the repo as a Claude plugin/project and Claude can load the skill from `skills/use-hln-api/`.

### Gemini CLI

Gemini CLI supports skills natively.

Install from a local checkout by targeting the canonical skill directory:

```bash
gemini skills install ./skills/use-hln-api --scope workspace
```

Or install from this Git repo by path:

```bash
gemini skills install https://github.com/HLnames/use-hln-api-skill.git --path skills/use-hln-api
```

To verify installation:

```bash
gemini skills list
```

N.B.: target `skills/use-hln-api/` for Gemini so it reads the canonical skill source rather than the generated Codex root copies.

### OpenClaw

OpenClaw uses AgentSkills-compatible skills from a `skills/` directory.

Install from a local checkout by copying canonical skill directory:

```bash
mkdir -p ~/.openclaw/skills/use-hln-api
cp -R ./skills/use-hln-api/. ~/.openclaw/skills/use-hln-api/
```

Or add at workspace scope:

```bash
mkdir -p /path/to/project/skills/use-hln-api
cp -R ./skills/use-hln-api/. /path/to/project/skills/use-hln-api/
```

N.B.: target canonical `skills/use-hln-api/` directory for OpenClaw rather than repo root, as it contains the generated Codex-compatible version.
