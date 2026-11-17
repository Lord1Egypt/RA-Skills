# Contributing

Thanks for your interest in improving `text-to-video`!

## Quick rules

- **Issues** — for bug reports / feature requests, please use [GitHub Issues](https://github.com/MinibeanAI/text-to-video/issues). Include:
  - Claude Code / claude.ai version
  - Node.js version (`node -v`)
  - Output of `hyperframes doctor`
  - Minimal reproduction steps
- **PRs** — fork → branch → commit → push → open a PR. Keep diffs small; one concern per PR.

## Development setup

```bash
git clone https://github.com/MinibeanAI/text-to-video
cd text-to-video
# Skill files live at the root; no build step.
# To test, point a Claude session at this directory and trigger the skill.
```

## Skill structure

```
text-to-video/
├── SKILL.md                    # core workflow (read this first)
├── README.md                   # human-facing
├── references/                 # deep dives
├── templates/                  # reusable scaffolds
└── scripts/                    # batch tooling (e.g. TTS)
```

## Editing the skill

- `SKILL.md` is the single source of truth for the agent workflow
- `references/*.md` is loaded only when the relevant phase is hit
- `templates/*.md` and `templates/*.html` are inserted into agent context at well-defined moments

If you add a new reference or template, mention it in `SKILL.md`'s "详细参考" section.

## Releasing

1. Bump version in `SKILL.md` frontmatter
2. Update `README.md` version badge + "版本" section
3. Tag: `git tag v1.x && git push --tags`
4. Build a new `.skill` bundle and attach to GitHub Release:
   ```bash
   zip -r text-to-video-v1.x.skill . -x "*.DS_Store" ".git/*"
   ```
