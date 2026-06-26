# Release Pipeline

## Never touch deployed files. The installer is the only deploy path.

Files at `~/.ldm/`, `~/.claude/`, `~/.openclaw/` are DEPLOYED by `ldm install`. Never edit them directly. Every change goes through the repo and the installer.

The plan for any feature must answer:
1. What source files change? (in the repo)
2. What does `ldm install` deploy? (templates, rules, docs, boot config, CLAUDE.md)
3. What needs to update for fresh install vs existing install?
4. What docs need updating?
5. What are ALL the files the installer touches on deploy?

Then: repo change, PR, merge, release, `ldm install`. That's the only path.

## Three steps. Never combine. Never skip.

| Step | What happens | What it means |
|------|-------------|---------------|
| **Merge** | PR merged to main | Code lands. Nothing else changes. |
| **Deploy** | wip-release + deploy-public.sh | Published to npm + GitHub. Not on your machine yet. |
| **Install** | Run the install prompt | Extensions updated on your machine. Only when Parker says "install." |

For alpha and beta tracks, agents install prereleases for validation: `ldm install --alpha` or `ldm install --beta`. That is test work, not owner dogfooding.

For stable/latest releases, after Deploy, STOP. Do not copy files. Do not npm install -g. Do not npm link. Do not run `ldm install` unless Parker explicitly asks. Parker dogfoods stable releases through the install prompt.

## The workflow

1. Create worktree, make changes, commit
2. Write RELEASE-NOTES on the branch (not after)
3. Push, create PR, merge (--merge, never squash)
4. `git checkout main && git pull`
5. `wip-release patch` (auto-detects release notes)
6. `deploy-public.sh` to sync public repo
7. Stop. Parker dogfoods: `Read https://wip.computer/install/wip-ldm-os.txt`

## Never run tools from repo clones

Installed tools are for execution. Repo clones are for development. Use the installed commands (`crystal`, `wip-release`, `mdview`, etc.), never run from source.

## On-demand reference

Before releasing, read `~/wipcomputerinc/library/documentation/how-releases-work.md` for the full pipeline with commands.
