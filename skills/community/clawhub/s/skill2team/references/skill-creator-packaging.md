# Skill Creator Packaging Notes

Skill2Team 1.9.2 is packaged in a Skill Creator style:

```text
skill2team/
  SKILL.md                  # lean entry instructions
  references/               # long docs loaded only when needed
  assets/prompt-templates/  # reusable continuation and registration prompts
  assets/runtime-templates/ # reusable Codex/generic package skeletons
  scripts/                  # deterministic helper scripts
  data/                     # machine-readable policies and contracts
  examples/                 # small text/json examples
  agents/                   # optional profile metadata for S2T service agents
  LICENSE                   # MIT No Attribution
  license.txt               # MIT-0 marker
  .clawhubignore            # excludes archives, binaries, caches, secrets
```

## Packaging rules

- Keep `SKILL.md` concise and trigger-focused.
- Put long design, runtime, and compliance guidance in `references/`.
- Put reusable prompt templates in `assets/prompt-templates/`.
- Put deterministic local helpers in `scripts/`.
- Keep the package text-only and UTF-8.
- Do not bundle generated output archives, caches, credentials, or binary/media artifacts.
- Do not add conflicting license terms in `SKILL.md`; use the MIT-0 files at package root.

## Context-on-demand rule

Load the minimum reference set for the current request. Package and conversion templates should be read only after design/package work asks for them.
