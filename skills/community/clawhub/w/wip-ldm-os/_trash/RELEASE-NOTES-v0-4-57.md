# Release Notes: wip-ldm-os v0.4.57

ldm install now deploys personalized docs to settings/docs/. Your system, your paths, your agents.

## What changed

- 14 doc templates in shared/docs/ (shipped in npm package)
- ldm init reads templates + config.json and generates personalized docs
- "Your System" sections show your actual agents, paths, harness config, timezone
- Reads from BOTH ~/.ldm/config.json (harnesses) and settings/config.json (agents, paths, org)

## Why

settings/docs/ had 14 manually-written docs that drifted from the repos. The docs pipeline plan (#227) establishes three layers: repo docs (generic) -> settings docs (personalized) -> website docs (public). This implements the personalization step.

## Issues closed

- #158 (ldm install: deploy docs to workspace settings)

## How to verify

```bash
npm install -g @wipcomputer/wip-ldm-os@latest
ldm init
grep "cc-mini" ~/wipcomputerinc/settings/docs/how-agents-work.md
grep "WIP Computer" ~/wipcomputerinc/settings/docs/what-is-ldm-os.md
```
