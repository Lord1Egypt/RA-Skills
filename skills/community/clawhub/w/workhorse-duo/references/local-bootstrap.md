# Workhorse Duo Local Bootstrap

Use this reference when the local machine does **not** already have `xiaoma` and `xiaoniu`.

Goal:
- create both agents if missing
- ensure the required cross-agent config exists
- validate that both agents can answer
- only then treat Workhorse Duo as ready for real tasks

## 1. Readiness target

Workhorse Duo is ready only if all of the following are true:
- `openclaw agents list` shows `xiaoma` and `xiaoniu`
- runtime config has:
  - `tools.agentToAgent.enabled = true`
  - `tools.sessions.visibility = "all"`
  - an `agentToAgent.allow` policy compatible with the target setup
- `openclaw agent --agent xiaoma --message ... --json` returns successfully
- `openclaw agent --agent xiaoniu --message ... --json` returns successfully

## 2. Create missing agents

Use the current workspace and current default model unless the operator explicitly wants different routing.

### Create xiaoma

```powershell
openclaw agents add xiaoma --workspace <current-workspace> --model <current-default-model> --non-interactive
```

### Create xiaoniu

```powershell
openclaw agents add xiaoniu --workspace <current-workspace> --model <current-default-model> --non-interactive
```

Then verify:

```powershell
openclaw agents list
```

## 3. Required config for cross-agent orchestration

Use the `gateway` tool to patch config.
Do **not** guess field names; inspect schema first if the environment is uncertain.

Required runtime state:

```json
{
  "tools": {
    "agentToAgent": {
      "enabled": true,
      "allow": ["*"]
    },
    "sessions": {
      "visibility": "all"
    }
  }
}
```

Notes:
- `allow: ["*"]` is acceptable for bootstrap/validation, but should be tightened later if the deployment needs stricter policy.
- after patching config, restart/reload the gateway and re-check runtime config.
- the exact published auto-fix helper flow is documented in `references/published-bootstrap-helper.md`.

## 4. Minimum smoke test

### xiaoma ping

```powershell
openclaw agent --agent xiaoma --message "你是小马（执行位）。请只回复：PONG" --timeout 120 --json
```

### xiaoniu ping

```powershell
openclaw agent --agent xiaoniu --message "你是小牛（验收位）。请只回复：PONG" --timeout 120 --json
```

Pass only if both return `PONG`.

## 5. Real smoke test

After ping success, run one real execute -> review loop:
- send a tiny real task to `xiaoma`
- summarize the result into a compact QA packet
- send that packet to `xiaoniu`
- require `验收没问题` or a concrete issue list

Do not claim installation success before this step passes.

## 6. Daily operating rule

After bootstrap succeeds:
- default to **asynchronous dispatch**
- do not block the main session waiting for workers during normal use
- tell the user the task has been handed off
- come back with results when workers finish

Use synchronous waiting only for debugging or smoke tests.
