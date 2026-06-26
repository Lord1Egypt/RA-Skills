# Troubleshooting

Use this file when the Synology problem is active right now and the next mistake could erase evidence or make recovery harder.

## First 5 Minutes

Collect evidence before changing state:

```bash
date
cat /etc.defaults/VERSION
df -h
df -i
free -m
cat /proc/mdstat
dmesg | tail -n 80
```

From DSM, capture:
- Storage Manager health, alerts, and active repair tasks
- package status and any failed backup or sync jobs
- the exact error text, not a paraphrase
- recent login, exposure, or update changes if the problem appeared suddenly

## Classify the Incident

Pick the dominant category first:

- storage pressure or disk health
- package failure or service crash
- backup failure or restore need
- network or remote access failure
- permissions or shared-folder access breakage
- suspected bad sync, deletion, or ransomware

The wrong category leads to the wrong fix, so classify before acting.

## Safe Escalation

- Read-only inspection first
- additive change second
- restart third
- reinstall fourth
- destructive cleanup last

If the user wants to skip straight to a risky fix, restate the evidence gap and the rollback cost.

## Evidence Template

Keep the incident note short and reusable:

```text
Time:
NAS model:
DSM version:
Workload affected:
What changed recently:
Symptoms:
Read-only findings:
Backups and snapshots available:
Next safe action:
Rollback:
```

## Patterns Worth Calling Out

- Low-space plus indexing backlog often looks like a generic slow NAS
- permission breakage after share changes often looks like network failure
- failed backup destination or expired credentials often looks like "Hyper Backup is broken"
- container mount mismatch often looks like image or app failure
- rebooting early can hide the real sequence of a failing disk, package, or network issue
