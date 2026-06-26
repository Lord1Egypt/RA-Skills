# Workspace Config Reference

## The `workspace` Object

Returned by `/api/tasks/pending` (top-level for workspace-scoped keys, per-task for account-scoped keys) and `/api/tasks/pickup`.

| Field | Type | Description |
|-------|------|-------------|
| `_id` | string | Workspace ID |
| `name` | string | Human-readable workspace name |
| `repoUrl` | string | GitHub repo URL (e.g. `https://github.com/org/repo`) |
| `githubToken` | string | GitHub PAT for this workspace (empty for public repos) |
| `agentConcurrency` | number | Max simultaneous agents; default 2 if not set |
| `defaultBranch` | string | Default base branch for PRs (fallback: `SC_DEFAULT_BRANCH` env var, then `main`) |

---

## Resolving Workspace Config (Both Key Types)

```javascript
// Safe for both workspace-scoped and account-scoped keys
const ws = task.workspace ?? response.workspace;
const repoUrl = ws.repoUrl;
const githubToken = ws.githubToken;
const concurrencyLimit = ws.agentConcurrency ?? 2;
const defaultBranch = process.env.SC_DEFAULT_BRANCH ?? ws.defaultBranch ?? "main";
```

**Never read `githubToken` from a local credentials file.** It may not exist on this machine. Always get it from the API response.

---

## Multi-Workspace Setup (Account-Scoped Key)

When using an account-scoped key:

- `/api/tasks/pending` returns tasks from **all workspaces** in a single response
- Each task embeds its own `workspace` object — no local workspace config needed
- Apply concurrency limits **per workspace independently**:

```javascript
// Group tasks by workspace, then dispatch up to limit for each
const byWorkspace = groupBy(tasks, t => (t.workspace ?? topLevelWs)._id);
for (const [wsId, wsTasks] of Object.entries(byWorkspace)) {
  const ws = wsTasks[0].workspace ?? topLevelWs;
  const limit = ws.agentConcurrency ?? 2;
  const running = countRunningAgentsFor(wsId); // count only agents for THIS workspace
  const slots = Math.max(0, limit - running);
  for (const task of wsTasks.slice(0, slots)) {
    dispatch(task, ws);
  }
}
```

**Do NOT count agents running for workspace A against workspace B's limit.**

---

## Branch Naming

Tasks always use branch `task/<taskId>`. The default base branch for PRs resolves as:

1. `SC_DEFAULT_BRANCH` env var (explicit override)
2. `workspace.defaultBranch` from API response
3. `main` (hardcoded fallback)

---

## Workspace Label in Spawn

Include workspace name in sub-agent label for easy identification in multi-workspace runs:

```javascript
sessions_spawn({
  label: `${agent.name}-${ws.name}-${task.title}`,
  ...
})
```
