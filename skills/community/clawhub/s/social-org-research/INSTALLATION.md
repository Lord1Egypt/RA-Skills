# Installation Guide

This skill ships in three forms:

1. As a directory in your local Hermes / OpenClaw / Claude Code skills folder (most common)
2. As a published GitHub repo at https://github.com/0xcjl/social-org-research
3. As a registered ClawHub package (slug: `social-org-research`)

## 1. Local install (Hermes)

If you already have this repo cloned to `~/.hermes/skills/social-org-research/`, you're done — Hermes auto-discovers skill folders.

```
ls ~/.hermes/skills/social-org-research/SKILL.md
```

Inside any Hermes conversation, `/skills list` should show "social-org-research".

## 2. Local install (OpenClaw / Claude Code)

```
ln -s ~/.hermes/skills/social-org-research ~/.openclaw/workspace/skills/social-org-research
```

Restart the agent to pick up the new skill.

## 3. Install via Hermes package manager

```
hermes skills install 0xcjl/social-org-research
```

## 4. Manual install from GitHub

```
git clone https://github.com/0xcjl/social-org-research.git ~/.hermes/skills/social-org-research
```

## 5. Install from ClawHub

```
clawhub install social-org-research
```

## Upgrade

```
hermes skills update social-org-research
```

or:

```
cd ~/.hermes/skills/social-org-research
git pull origin main
```

## Verification

```
ls ~/.hermes/skills/social-org-research/SKILL.md
python3 -c "import yaml; yaml.safe_load(open('~/.hermes/skills/social-org-research/SKILL.md').read().split('---')[1])"
```

Both commands should succeed silently.

## Uninstall

```
rm -rf ~/.hermes/skills/social-org-research
```
