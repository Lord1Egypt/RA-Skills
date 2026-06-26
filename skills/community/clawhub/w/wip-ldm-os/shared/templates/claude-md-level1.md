# Global Instructions for Claude Code

## Writing Style

Never use em dashes. Use periods, colons, semicolons, or ellipsis (...) instead.
Timezone: PST (Pacific), 24-hour clock. Parker is in Los Angeles.

## Don't Hedge

Never ask "should I stop?", "is this too much?", "what should we do now?", or "do you want me to continue?". If you have work to do, do it. If you're stuck, say what you're stuck on specifically. Don't express existential doubt about the task. Don't ask permission to keep working. Don't narrate your own uncertainty. Just work.

## Co-Authors on Every Commit

Read co-author lines from `~/.ldm/config.json` coAuthors field. All contributors listed on every commit. No exceptions.

## 1Password CLI: Always Use Service Account Token

Never call `op` bare. Always prefix with the SA token:
```bash
OP_SERVICE_ACCOUNT_TOKEN=$(cat ~/.openclaw/secrets/op-sa-token) op item get "Item Name" --fields label=fieldname
```

## Never Run Tools From Repo Clones

Installed tools are for execution. Repo clones are for development. Use installed commands (`crystal`, `wip-release`, `mdview`), never run from source.

## Shared File Protection

Never use Write on SHARED-CONTEXT.md or shared workspace files. Always use Edit to append or update specific sections. Overwriting destroys context that both agents depend on.

## Memory-First Rule

Before reaching for any external service or workaround: search memory first. Use `crystal_search`, `lesa_conversation_search`, or `lesa_memory_search`.

## Dev Conventions

For git workflow, releases, worktrees, and repo conventions: read `~/wipcomputerinc/library/documentation/` on demand when doing repo work. Key docs:
- `how-worktrees-work.md` ... git worktrees, the convention, commands
- `how-releases-work.md` ... the full release pipeline
- `system-directories.md` ... what lives where
- Also read `~/.ldm/shared/dev-guide-wipcomputerinc.md` for org-specific conventions
