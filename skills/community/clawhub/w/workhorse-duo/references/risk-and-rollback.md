# Risk and Rollback

Use this reference before enabling auto-fix or publishing Workhorse Duo to other users.

## 1. Bootstrap-safe defaults vs long-term defaults

Bootstrap-safe defaults may temporarily use:
- `tools.agentToAgent.enabled = true`
- `tools.sessions.visibility = "all"`
- `tools.agentToAgent.allow = ["*"]`

Why:
- they reduce friction during first install and validation
- they make it easier to prove the workflow really works

These are **not automatically the best long-term production posture**.
After validation, tighten policy if the deployment requires stronger isolation.

## 2. Auto-fix risk

The published helper flow in `references/published-bootstrap-helper.md` will:
- modify `~/.openclaw/openclaw.json`
- create a backup beside that file
- set bootstrap-safe cross-agent config values
- restart the gateway

Use this mode only when the operator accepts config mutation and restart side effects.

## 3. Recommended post-bootstrap tightening

After Workhorse Duo is proven ready, consider tightening:
- replace `allow: ["*"]` with a narrower policy suited to the deployment
- reduce `tools.sessions.visibility` if cross-agent visibility wider than necessary is not desired
- review whether `exec.security = full` is appropriate for the target environment

## 4. Rollback

If you want to remove Workhorse Duo bootstrap changes:

### Remove agents

```powershell
# remove the xiaoma/xiaoniu entries manually from ~/.openclaw/openclaw.json, or restore from backup
```

### Restore config from backup

```powershell
Copy-Item "$HOME\.openclaw\openclaw.json.bak" "$HOME\.openclaw\openclaw.json" -Force
openclaw gateway restart
```

### Or manually revert these fields

```json
{
  "tools": {
    "agentToAgent": {
      "enabled": false,
      "allow": []
    },
    "sessions": {
      "visibility": "tree"
    }
  }
}
```

Choose the rollback shape that matches the operator’s original environment.

## 5. Release bar

Do not publish Workhorse Duo as a broadly reusable skill unless all of the following are true:
- bootstrap steps are documented
- auto-fix behavior is explicit
- rollback is documented
- examples match the published default route
- a fresh operator can understand setup, use, and recovery without hidden chat context
