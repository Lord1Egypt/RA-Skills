# Host Parity Policy

This repo participates in the Sage Router, Remnic, Ollama, OpenClaw, and Umbrel host fleet. Treat parity as service and integration parity, not data parity.

Parity means:

- Sage Router health reports configured providers, provider auth sources, and provider key counts without exposing secret values.
- Provider policy enables keyed providers and disables only intentionally unsupported providers.
- Remnic is healthy on each host and is wired to that host's own OpenClaw/Codex identity.
- Ollama is reachable through the host's intended service path and exposes local and/or cloud model manifests as appropriate.
- Umbrel app shortcuts and app proxies target the dashboard or API surface intended for that app, with no port drift.

Parity does not mean copying Remnic memory between hosts. `Cyber`, `Umbrel`, `mntd3593`, `mntd0809`, `sovereign`, and any other OpenClaw host can have unique agents, containers, sessions, and Remnic memory. Do not synchronize or overwrite host memory unless the operator explicitly asks for a migration.

GCloud edge policy:

- The GCloud Sage Router edge may remain a lightweight edge/failover host.
- It does not need Remnic or local Ollama.
- It may use an Ollama Cloud capable fallback/upstream rather than carrying the full provider set locally.

Before committing changes that affect Sage Router, Remnic, Ollama, OpenClaw, Umbrel app packaging, or Cyber gateway compose files, verify the relevant live host health and update the matching Dropbox project branch or worktree.

## Local hook

This repo includes an advisory pre-commit reminder at `.githooks/pre-commit`.
Enable it in a new clone with:

```bash
git config core.hooksPath .githooks
```

The hook prints parity reminders only; it does not block commits.
