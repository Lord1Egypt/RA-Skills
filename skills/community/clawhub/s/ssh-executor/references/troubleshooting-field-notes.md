# Troubleshooting Field Notes

Production deployment and audit remediation learnings.

---

## Multiplexing + stale group membership

**Symptom:** `usermod -aG sudo <user>` succeeds, but sudo still fails.
**Cause:** ControlMaster socket from before group change.
**Fix:** `ssh -O exit user@host` then retry — new session gets new groups.

---

## UserKnownHostsFile /dev/null

**Symptom:** StrictHostKeyChecking=yes rejects known hosts.
**Cause:** SSH config has `UserKnownHostsFile /dev/null`.
**Fix:** Skill now overrides to real known_hosts when strict mode is active (v2.2.1+).

---

## trap + shred + set -e = phantom exit 1

**Symptom:** ssh-keys.sh restore prints success but returns exit 1.
**Cause:** EXIT trap runs `shred -u` on already-deleted file, `set -e` converts to exit 1.
**Fix (v2.2.1):** `rm -f` in trap, shred runs explicitly in code path.

---

## Sudo requires --confirm-dangerous (v2.3.1+)

**Before:** --sudo auto-set CONFIRM_DANGEROUS=1.
**Now:** --sudo blocks with exit 99 unless --confirm-dangerous is passed.
**LLM flow:** present command → user approves → retry with --confirm-dangerous.

---

## VAULT_RESOLVER_BIN validation (v2.3.1)

**Risk:** Env var flows directly to subprocess.run.
**Fix:** `shutil.which()` for bare names, `os.path.isfile()` + `os.access(X_OK)` for paths.

---

## Paramiko RejectPolicy + known_hosts (v2.3.1)

**Before:** RejectPolicy without loaded known_hosts meant everything rejected.
**Fix:** Load `~/.ssh/known_hosts` + `/etc/ssh/ssh_known_hosts` into Paramiko client.
