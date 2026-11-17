---
name: soundclaw
description: Onboard and operate SoundClaw through one thin OpenClaw-facing product and the promoted runtime CLI.
version: 1.0.0
homepage: https://github.com/catholicbeer/soundclaw-skills/tree/main/skills/soundclaw
metadata:
  openclaw:
    os: ["linux"]
---

# SoundClaw

Use this skill for every SoundClaw operator request. It is the single
OpenClaw-facing product: first-use onboarding and later normal capability
routing belong to this same installed skill.

## First-Run And Readiness Behavior

- When backend readiness has not been established in the current conversation,
  check for `soundclawctl` on `PATH`; if it is absent, check
  `/opt/soundclaw/runtime/current/bin/soundclawctl`.
- If neither executable exists, say that the SoundClaw backend does not appear
  to be installed. Point only to the public GitHub Releases page at
  `https://github.com/catholicbeer/soundclaw-release/releases` and tell the
  operator to use the `install.sh` wrapper inside one verified public
  `soundclaw-pi-release-<release-id>.tar.gz` bundle. Stop there. Do not fetch,
  install, repair, copy, or sync backend content.
- If an executable exists, run `<soundclawctl> runtime status --json`. Treat
  that runtime-owned result as authoritative. Report ready, degraded, or
  unavailable without attempting host repair.
- Once readiness is established, handle later supported requests through this
  same skill. Do not require or route to separately installed SoundClaw leaf
  skills.

## Capability Routing

- Resolve assets with `soundclawctl library list [--json]` and
  `soundclawctl library show --asset <id> [--json]`.
- Resolve logical outputs with `soundclawctl outputs list [--json]`,
  `soundclawctl outputs show --output <id> [--json]`, and
  `soundclawctl config defaults [--json]` when a default is relevant.
- Play with
  `soundclawctl playback play --asset <id> --output <id> [--fade-in-ms <n>] [--json]`.
  Stop with
  `soundclawctl playback stop --output <id> [--fade-out-ms <n>] [--json]`.
- Inspect or change global volume with `soundclawctl volume show [--json]` and
  `soundclawctl volume set-global --global-volume-percent <0-100> [--json]`.
  Explain any runtime-reported reload requirement; never hide a reload.
- Use `soundclawctl runtime status [--json]`,
  `soundclawctl runtime doctor [--json]`, and
  `soundclawctl config validate [--json]` for health and configuration checks.
- Report backend deployment identity with
  `soundclawctl deployment status [--json]`. Keep this separate from the
  ClawHub product version and provenance.
- For deliberate low-risk output or zone administration, use only the
  promoted `soundclawctl outputs`, `soundclawctl zones`, and explicit
  `soundclawctl runtime reload [--json]` command shapes listed in the local
  reference. Clarify the target and proposed mutation before acting.
- For one on-demand Layer, use the promoted `soundclawctl familiar
  run-layer` or `stop-layer` command. For a bounded Scene, use the promoted
  `soundclawctl scene apply/show/explain/stop` boundary. Do not own execution
  state, retries, policy, or replay.
- Guide source-preserving library ingest only through a promoted
  `soundclawctl library ingest [--json]` or public-bundle pi-kit flow after
  explicit operator approval. Do not browse arbitrary paths or edit the
  deployed library directly.
- Use the optional private `soundclaw-feedback` capability only when it is
  present and the operator explicitly requests feedback lifecycle work. Never
  store feedback in this public skill.

## General Behavior

- Ask only for missing asset, output, Scene, Layer, volume, or topology facts
  needed for a safe deterministic command.
- Prefer the smallest promoted read needed to resolve ambiguity.
- Relay runtime-owned results and errors. Do not claim success from intent or
  marker checks alone.
- Keep skill provenance, backend deployment identity, and runtime health as
  separate facts.

## Out Of Scope

- Backend installation, update, repair, rollback, or service manipulation
- Copying, rsyncing, Git-syncing, or shadowing installed skills
- Private Web UI routes, DOM state, runtime IPC, or host-file parsing
- Invented runtime commands or local substitutes for unavailable capabilities
- Hidden retries for mutating commands

## Local References

- Read `{baseDir}/references/README.md` for the operator job, guardrails, and intent boundary.
- Read `{baseDir}/references/examples.md` for example requests and expected behavior.
- Read `{baseDir}/references/compatibility.md` for runtime dependency and packaging notes.
