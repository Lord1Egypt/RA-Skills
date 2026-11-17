# P0: Day 63 hand-deploy was deleted by website deploy.sh

> Filed by: Lēsa (oc-lesa-mini) on 2026-04-30

## Status

Open. Recovery and deploy guard are in progress.

## Summary

The Day 63 microsite was live at `https://wip.computer/day-63/` after a direct VPS deploy on 2026-04-04. It was later deleted by a normal `wip-websites-private/deploy.sh` run on 2026-04-28 because the canonical deploy source did not contain `wip.computer/day-63/` and the script uses `rsync --delete`.

This is a production data-loss class bug. Any content hand-deployed to `/var/www/wip.computer/public_html/` outside `wip-websites-private/wip.computer/` can be silently deleted by the next canonical deploy.

## Impact

- `https://wip.computer/day-63/` disappeared after Parker had seen it and shared it.
- The source content survived locally in `/Users/lesa/wipcomputerinc/repos/day-63/`.
- The live production path did not survive because it was never committed to the deploy source of truth.
- The same failure mode can affect any future hand-deployed site, install file, or artifact.

## Evidence

### Apr 4 deploy that made Day 63 live

CC transcript evidence shows a failed first attempt at 2026-04-04 12:11:10 PDT, then this successful direct VPS deploy at 2026-04-04 12:11:28 PDT:

```bash
ssh wip-vps 'sudo mkdir -p /var/www/wip.computer/public_html/day-63/images && \
             sudo chown parker:parker /var/www/wip.computer/public_html/day-63 -R' && \
  scp -r /Users/lesa/wipcomputerinc/repos/day-63/*.html \
         /Users/lesa/wipcomputerinc/repos/day-63/*.md \
         /Users/lesa/wipcomputerinc/repos/day-63/*.json \
         /Users/lesa/wipcomputerinc/repos/day-63/*.txt \
         wip-vps:/var/www/wip.computer/public_html/day-63/ && \
  scp -r /Users/lesa/wipcomputerinc/repos/day-63/images/* \
         wip-vps:/var/www/wip.computer/public_html/day-63/images/
```

Source transcript: `~/.claude/projects/-Users-lesa-wipcomputerinc/9f25801b-0cd4-4d75-99a7-47cafe1a2385.jsonl`.

Key problem: this deploy wrote straight to `/var/www/wip.computer/public_html/day-63/`. It skipped `wip-websites-private/wip.computer/day-63/`, skipped git, and skipped `deploy-manifest.json`.

### Apr 28 deploy that deleted Day 63

At 2026-04-28 11:48:30 PDT, CC ran:

```bash
cd .worktrees/wip-websites-private--cc-mini--deploy-origin && \
  bash deploy.sh 2>&1 | tail -30
```

Source transcript: `~/.claude/projects/-Users-lesa-wipcomputerinc/df335668-3a73-4f53-9d80-fbcd44da7a71.jsonl`.

The clean `wip-websites-private` source tree did not contain `wip.computer/day-63/`. `deploy.sh` runs two destructive syncs:

```bash
rsync -avz --delete ... "$SITE_DIR/" "$REMOTE:$STAGING_DIR/"
ssh $REMOTE "sudo rsync -a --delete $STAGING_DIR/ $REMOTE_PATH ..."
```

That means the deploy source became the complete truth for the VPS. Since `day-63/` was remote-only, rsync deleted it. The `tail -30` pipe likely hid any `deleting day-63/...` lines from the agent.

## Root Cause

Day 63 was deployed outside the canonical website source of truth. The canonical deploy script then correctly mirrored its source tree, but that source tree was incomplete.

The deeper bug is that `deploy.sh` allows destructive deletion of remote-only production paths without a preflight diff, manifest check, snapshot, or explicit operator acknowledgement.

## Required Fixes

1. Restore Day 63 into `wip-websites-private/wip.computer/day-63/` and add a `/day-63/` entry to `deploy-manifest.json`.
2. Harden `wip-websites-private/deploy.sh` so normal deploys fail before deleting remote-only top-level paths.
3. Require an explicit override, such as `--allow-deletes`, for reviewed deletions.
4. Stop piping deploy output through `tail` for destructive deploys. Full rsync output must be visible or logged.
5. Add a permanent rule: never hand-deploy into `/var/www/wip.computer/public_html/`. New public paths must land in `wip-websites-private` first.
6. Add a follow-up snapshot mechanism before destructive production deploys.

## Recovery Plan

1. Open a `wip-websites-private` PR that restores `wip.computer/day-63/`, adds the manifest entry, and patches `deploy.sh` with a remote-only deletion preflight.
2. Merge normally, never squash.
3. Pull local `main` after merge.
4. Run `bash deploy.sh --dev` from merged main and smoke test `dev.wip.computer/day-63/`.
5. Run production deploy only after Parker explicitly approves.

## Follow-Up

After Day 63 is recovered, investigate and restart Lēsa's `/usr/lesa/` blog and `/usr/lesa/surprises/` pipeline. The current known issues are stale index content, untracked surprise folders, and crons disabled during the Apr 6 to Apr 7 cost-control incident.
