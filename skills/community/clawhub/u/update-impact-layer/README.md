# Clawkeeper 🦞

An OpenClaw skill that keeps a small, machine-local impact ledger around the
native updater. It tracks only what OpenClaw cannot know itself: live local
overrides, temporary compatibility obligations, and quiet external seams that
need a bounded post-update proof.

It does **not** replace `openclaw update`, native admission, backups, restart
coordination, reports, repair, recovery, or cleanup.

## Install

```bash
openclaw skills install @clawSean/update-impact-layer
```

Or clone this repository into your OpenClaw workspace as
`skills/openclaw-update`.

## Use

Ask your agent to prepare or verify an OpenClaw update. The skill first follows
the installed CLI and docs, then selects only the local impact entries relevant
to that update.

Keep private hostnames, account names, installed paths, and internal project
links in your own local ledger—not in the shared skill.

## Source

This repository and the
[SkillReef catalog](https://github.com/clawSean/skillreef) are generated from
the same scrubbed skill source and checked for drift before publication.
