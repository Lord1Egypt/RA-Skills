# MIT-0, OpenClaw, and ClawHub Compliance Notes

Skill2Team 1.9.2 is prepared as a text-only OpenClaw/ClawHub-oriented skill package.

## Package shape

- `SKILL.md` is the lean entry file.
- `references/` contains long documentation loaded on demand.
- `assets/prompt-templates/` contains reusable prompt templates.
- `assets/runtime-templates/` contains reusable Codex/generic package skeletons.
- `scripts/` contains deterministic helper scripts.
- `data/` contains machine-readable policies, manifests, and contracts.
- `examples/` contains small text/json examples.
- `.clawhubignore` excludes archives, binary/media files, caches, and local secrets.

## Frontmatter policy

- `name: skill2team`
- `description` is a short one-line trigger phrase.
- `version: 1.9.2`
- global discovery metadata is present.
- `metadata.openclaw.emoji` uses a real emoji.
- No conflicting `license:` override is included.

## MIT-0 licensing

- `LICENSE` contains MIT No Attribution text.
- `license.txt` states `MIT-0`.
- Do not add restrictive terms or attribution requirements to `SKILL.md` or generated package docs.

## Local QA

```bash
python scripts/validate_package.py .
```

Passing local QA is not the same as a live ClawHub publish acceptance, but it checks the package shape, metadata, text-only constraints, MIT-0 files, and Skill2Team-specific invariants.
