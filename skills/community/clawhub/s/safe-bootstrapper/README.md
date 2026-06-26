# safe-bootstrapper

Deterministic setup and remediation for installed OpenClaw skills. Part of
[SAFE: Skilled Agent Fuzzing Engine](https://github.com/RiemaLabs/safe).
Resolves a target skill, applies sandbox-local remediation when safe, and
produces a structured setup report before fuzzing.

This skill is sandbox-only. It is designed to run inside the OpenClaw
`fuzzer` sandbox and should not fall back to host execution.

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

```bash
openclaw agent --agent fuzzer --timeout 600 \
  --message '/skill safe-bootstrapper target=<skill-slug>'
```

## Notes

- `target` is a skill name, not an agent id.
- `safe-bootstrapper` owns deterministic local remediation (git init, env-file
  creation, local state directories, reruns). It does not install dependencies
  or perform network downloads.
- Run `safe-bootstrapper` before `safe-fuzzer` so the target is locally
  runnable before behavioral probing begins.
- If the sandbox lacks runtime dependencies such as `node`, `safe-bootstrapper`
  should report a setup blocker instead of silently falling back to the host.
