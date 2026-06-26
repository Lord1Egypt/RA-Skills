# Security Review

The goal is to make `skill-port` safe to publish and safe to use on untrusted skills. Do not claim guaranteed approval from indexes. `skills.sh` performs routine audits and shows risk results, but still tells users to review skills before installing.

## Published Skill Safety

The `skill-port` skill itself should:

- Avoid install lifecycle hooks and auto-running scripts.
- Avoid bundled credentials, API keys, tokens, or private URLs.
- Avoid obfuscated code.
- Avoid network calls in bundled scripts.
- Avoid destructive filesystem operations.
- Keep scripts small, readable, and read-only by default.
- Require explicit user approval before cloning remote repos, installing dependencies, or writing outside the selected output path.

## Audit Signals

Flag these in inspected sources:

- Secret-like values: API keys, tokens, private keys, cloud credentials.
- Destructive commands: recursive forced deletes, hard repository resets, broad permission changes, disk formatting, recursive deletes.
- Shell execution: process spawning, shell command runners, dynamic code evaluation.
- Network activity: URLs, curl, wget, fetch, requests, axios.
- Install hooks: package manager lifecycle hooks, package manager scripts, plugin lifecycle hooks.
- Credential movement: environment dumping, SSH/cloud config directories, credential-manager access, token files.
- Hidden or binary files that are not obviously assets.
- Large files that should be assets/templates rather than context.

## Risk Levels

- `low`: plain instructions and safe static assets.
- `medium`: scripts, network endpoints, MCP dependencies, binaries, or many hidden files.
- `high`: secret-like strings, destructive commands, obfuscation, credential access, install hooks, or auto-execution behavior.

## Safe Handling

- Read files; do not execute them.
- Prefer deterministic reports over subjective conclusions.
- Do not suppress findings because a source is popular.
- For financial, legal, medical, or regulated workflows, preserve human-review and non-advice disclaimers.
