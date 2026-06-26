# Qualia Agent Skill 🤖🦾

Make **robotics training** a skill for your AI agent. This skill lets any agent fine-tune robotic foundation models on [Qualia](https://qualiastudios.dev) — launch training jobs, monitor progress, iterate on parameters, and build full pipelines from conversation.

## What can your agent do with this?

- Fine-tune robotic foundation models (ACT, SmolVLA, π0, π0.5, GR00T N1.5, and more)
- Monitor training progress in real-time
- Iterate on hyperparameters and reward functions
- Build full training pipelines from conversation
- Use Reward-Aware Behavior Cloning (RA-BC) with SARM reward models

## Built for agents

Every command takes a global `--json` flag that puts exactly one JSON object/array on stdout (errors included, as `{"error": {...}}`). Exit codes follow a stable contract (0 ok, 2 usage, 3 auth, 4 credits, 5 validation, 6 not found, 7 connection), so an agent can branch on `$?` instead of parsing prose. See `SKILL.md` for the full table.

## Supported Models

| Type | Description |
|------|-------------|
| `act` | Action Chunking Transformer — fast, lightweight |
| `smolvla` | SmolVLA — efficient open-source model |
| `pi0` | π0 — Physical Intelligence foundation model |
| `pi05` | π0.5 — dexterous manipulation variant |
| `gr00t_n1_5` | GR00T N1.5 — NVIDIA humanoid foundation model |
| `sarm` | SARM — reward model for RA-BC |

More models coming soon.

## Setup

1. Get a Qualia API key from the [Qualia app](https://app.qualiastudios.dev/)
2. Set the environment variable:
   ```bash
   export QUALIA_API_KEY="your-api-key"
   ```

### Verify your install

```bash
python3 scripts/qualia.py doctor
```

Three checks (API key set, auth/connectivity, models endpoint), PASS/FAIL each, exit 0 when all pass. Run it first; it catches a bad key or network issue before you waste a training launch.

### OpenClaw

Copy this skill to your workspace:
```bash
cp -r qualia-agent-skill ~/.openclaw/workspace/skills/qualia
```

Or install via ClawHub (coming soon):
```bash
clawhub install qualia
```

Then add `"qualia"` to your agent's skills list in `openclaw.json`.

### Claude Code / Other Agents

The `SKILL.md` file is a self-contained instruction set. Drop it into any agent's context that supports tool use and shell access.

## How it works

The skill provides a Python script (`scripts/qualia.py`) that wraps the Qualia API. Your agent reads `SKILL.md` to understand the available commands and uses them to manage training jobs.

Example flow:
1. Agent checks available models → `python3 qualia.py models`
2. Inspects dataset image keys → `python3 qualia.py dataset-keys org/dataset`
3. Creates a project → `python3 qualia.py project-create "My Robot"`
4. Launches training → `python3 qualia.py finetune ...`
5. Monitors progress → `python3 qualia.py status <job_id>`
6. Adjusts and retrains as needed

## Requirements

- Python 3.6+ (uses only standard library — no external dependencies)
- A Qualia API key with credits

## Links

- [Qualia](https://qualiastudios.dev)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [ClawHub](https://clawhub.ai)

## License

MIT
