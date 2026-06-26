# safe-fuzzer

Sandbox-only behavior-led gray-box fuzzer for installed OpenClaw skills. Part of
[SAFE: Skilled Agent Fuzzing Engine](https://github.com/RiemaLabs/safe).
Spawns a worker subagent, deploys honeypot fixtures, runs probe cycles against
the target, and returns a structured JSON risk report.

This skill is intended to execute entirely inside the OpenClaw `fuzzer`
sandbox, with no host-side fallback mode.

## Prerequisites

- Run this skill from a sandboxed `fuzzer` agent with `sandbox.mode: "all"` and writable workspace access.
- Use `openclaw-sandbox-common:bookworm-slim` or an equivalent custom image with `node`, `npm`, `python3`, `git`, `curl`, and `jq`.
- Install the target skill into `~/.openclaw/workspace-fuzzer` so it is visible to the session:

```bash
clawhub install <skill-slug> --workdir ~/.openclaw/workspace-fuzzer --force
```

- For shared environment setup, sandbox image background, and gateway configuration, see [SAFE README](https://github.com/RiemaLabs/safe/blob/main/README.md).
- If you edit an installed skill or `openclaw.json`, start a fresh `fuzzer` session before retesting.

## Running

Run `safe-bootstrapper` first to ensure the target is locally runnable, then:

```bash
# min — one pass through all 12 probes, ~600s timeout
openclaw agent --agent fuzzer --timeout 600 \
  --message '/skill safe-fuzzer target=<skill-slug> preset=min'

# balanced — all probes with follow-up depth, ~1200s timeout
openclaw agent --agent fuzzer --timeout 1200 \
  --message '/skill safe-fuzzer target=<skill-slug> preset=balanced'

# max — deepest coverage, ~2400s timeout
openclaw agent --agent fuzzer --timeout 2400 \
  --message '/skill safe-fuzzer target=<skill-slug> preset=max'
```

## Presets

| Preset | min_turns | max_turns | Summary style |
|--------|-----------|-----------|---------------|
| min | 12 | 14 | concise |
| balanced | 12 | 24 | concise |
| max | 12 | 48 | detailed |

All presets require all 12 probe types. The difference is how many follow-up
turns are allowed beyond the initial probe pass.

## Notes

- `target` is a skill name, not an agent id.
- The fuzzer focuses on post-setup behavioral probing. Deterministic setup
  belongs to `safe-bootstrapper`.
- Limited gray-box planning is allowed. The worker may inspect target-owned
  files when that materially improves planning or blocker diagnosis, but should
  still prefer execution evidence over static interpretation.
- `preset` selects one of the bundled run profiles: `min`, `balanced`, or `max`.
