#!/usr/bin/env python3
"""Prune stale/done cron and subagent session entries from sessions.json."""
import json, sys, time

path = sys.argv[1]
stale_sub_h = float(sys.argv[2])
stale_cron_h = float(sys.argv[3])
now = time.time()

d = json.load(open(path))
sessions = d.get("sessions", d)
to_prune = []

for k, v in sessions.items():
    updated = v.get("updatedAt", 0)
    if updated > 1e12: updated /= 1000
    if not updated: continue
    age_h = (now - updated) / 3600
    status = v.get("status", "")

    if ":subagent:" in k:
        # Done sub-agents: prune immediately (no grace period needed)
        if status == "done":
            to_prune.append(k)
        # Running/unknown sub-agents: prune after stale threshold
        elif age_h > stale_sub_h:
            to_prune.append(k)
    elif ":cron:" in k and age_h > stale_cron_h:
        to_prune.append(k)

if to_prune:
    for k in to_prune:
        del sessions[k]
    json.dump(d, open(path, "w"), indent=2)

print(len(to_prune))
