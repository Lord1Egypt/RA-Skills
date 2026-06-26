# Project Notes for Claude

## Workflow rules

- **Never** commit, push, or publish to ClawHub without explicit user permission. Always ask first.

## Reference Documentation

Before answering any question about ClawHub commands, SKILL.md format, or skill configuration — fetch and read the relevant documentation page first:

- https://docs.openclaw.ai/ OpenClaw docs.
- https://docs.openclaw.ai/tools/clawhub — ClawHub CLI commands (install, update, list, publish, etc.)
- https://docs.openclaw.ai/tools/skills — SKILL.md structure and frontmatter spec
- https://docs.openclaw.ai/tools/skills-config — skill configuration and openclaw.json
- https://yandex.cloud/ru/docs — Yandex Cloud documentation (SpeechKit, IAM, service accounts)

### ClawHub CLI reference (from docs)

```
clawhub install <slug>
clawhub update <slug>
clawhub update --all
clawhub update --version <version>   # single slug only
clawhub update --force               # overwrite when local files don't match published version
clawhub list                         # reads .clawhub/lock.json

clawhub publish <path>               # publish skill from folder
  --slug <slug>                      # skill slug (unique ID)
  --name <name>                      # display name shown in search
  --version <version>                # semver (e.g. 1.1.3)
  --changelog <text>                 # changelog text
  --tags <tags>                      # comma-separated tags (default: "latest")
  --fork-of <slug[@version]>         # mark as a fork of an existing skill
```

## Key conventions

- `SKILL.md` frontmatter `metadata` must be a **single-line JSON** with the `openclaw` namespace:
  ```
  metadata: {"openclaw": {"requires": {"bins": [...], "env": [...]}, "primaryEnv": "..."}}
  ```
- `name` in SKILL.md frontmatter is the registry package ID (e.g. `sergei-mikhailov-stt`), not a display name
- Display name is the `#` heading in the body of SKILL.md
