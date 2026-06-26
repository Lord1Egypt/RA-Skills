# First-Run Path

Use this reference when a user installs Workhorse Duo and wants the shortest path from "installed" to "first successful real task".

## Goal

A first-time operator should be able to answer four questions quickly:
1. Are `xiaoma` and `xiaoniu` present?
2. Is cross-agent orchestration configured?
3. Can both agents answer a ping?
4. Can one real execute -> review loop complete?

## First-run sequence

### Step 1 — Bootstrap

Use the published helper in `references/published-bootstrap-helper.md`.
If the operator prefers a local script workflow, copy the PowerShell block from that file into `bootstrap-workhorse-duo.ps1` and run:

```powershell
./bootstrap-workhorse-duo.ps1
```

If config is missing and the operator accepts auto-fix + restart:

```powershell
./bootstrap-workhorse-duo.ps1 -AutoFixConfig
```

Expected outcome:
- the script clearly says `READY` or `NOT READY`
- if not ready, the blocking reason is explicit

### Step 2 — Ping validation

If the operator wants to validate manually:

```powershell
openclaw agent --agent xiaoma --message "You are Xiaoma, the execution worker. Reply only: PONG" --timeout 120 --json
openclaw agent --agent xiaoniu --message "You are Xiaoniu, the QA worker. Reply only: PONG" --timeout 120 --json
```

Expected outcome:
- both return `PONG`

### Step 3 — First real loop

Run one tiny real task through Xiaoma, then summarize the result for Xiaoniu.
Use a task small enough that the operator can verify the result manually if needed.

### Step 4 — Normal daily use

After the first real loop succeeds:
- dispatch asynchronously
- do not block the main session
- proactively report back when workers finish

## What success looks like

The installation should feel complete only when:
- bootstrap is done
- ping works
- one real loop works
- the operator understands the daily async workflow
