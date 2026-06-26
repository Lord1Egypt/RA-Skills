###### WIP Computer

# Repo Init

Scaffold the standard `ai/` directory in any repo. Plans, notes, ideas, dev updates, todos. One command.

## What it does

- **New repo:** Creates the full `ai/` directory structure
- **Existing repo:** Moves old `ai/` contents to `ai/_sort/ai_old/` so you can sort at your own pace
- Nothing is deleted

## The `ai/` directory

```
ai/
  plan/              architecture plans, roadmaps
  dev-updates/       what was built, session logs
  todos/
    PUNCHLIST.md     blockers to ship
    inboxes/         per-agent action items
  notes/             research, references, raw conversation logs
```

The `ai/` folder is the development process. It is not part of the published product. Public repos exclude it via deploy-public.sh.

## Usage

```bash
node tools/wip-repo-init/init.mjs /path/to/repo
```

## Interfaces

- **CLI**: Run from terminal
- **Skill**: SKILL.md for agent instructions

## Part of [AI DevOps Toolbox](https://github.com/wipcomputer/wip-ai-devops-toolbox)
