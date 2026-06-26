---
name: prts-sandbox
description: Isolated Kali Linux sandbox for running pentest tools and risky commands safely.
metadata: {"openclaw":{"emoji":"🛡️","requires":{"bins":["bash","curl","jq"]}}}
---

# PRTS Sandbox

An isolated **Kali Linux 2025.4** container. All pentest tools and risky commands run here — never on the host.

## Script path
```
~/.openclaw/skills/prts-sandbox/scripts/sandbox-cmd.sh
```

---

## When to use sandbox vs host

| Task | Where |
|------|-------|
| Running pentest tools (nmap, hydra, sqlmap, etc.) | ✅ Sandbox |
| Executing downloaded/unknown scripts | ✅ Sandbox |
| Anything that could break the host | ✅ Sandbox |
| Editing memory/SOUL.md/agent files | ❌ Host |
| Reading internal agent files | ❌ Host |

---

## How to run a command (3 steps)

**Step 1 — Check if sandbox is running:**
```bash
~/.openclaw/skills/prts-sandbox/scripts/sandbox-cmd.sh status
# Returns: true (running) or false (stopped)
```

**Step 2 — Start it if stopped (or Reset if error occurs):**
```bash
~/.openclaw/skills/prts-sandbox/scripts/sandbox-cmd.sh start
# CRITICAL RULE: If the start command fails with an error stating "the container name 'protocol-space-active' is already in use", you MUST run `reset`:
~/.openclaw/skills/prts-sandbox/scripts/sandbox-cmd.sh reset
```

**Step 3 — Execute your command:**
```bash
~/.openclaw/skills/prts-sandbox/scripts/sandbox-cmd.sh exec nmap -sV 192.168.1.1
~/.openclaw/skills/prts-sandbox/scripts/sandbox-cmd.sh exec sqlmap -u "http://target/page?id=1"
~/.openclaw/skills/prts-sandbox/scripts/sandbox-cmd.sh exec sh -c "hydra -l admin -P /wordlist.txt ssh://192.168.1.10"
```

---

## Available tools

| Category | Tools |
|----------|-------|
| Recon | `nmap`, `masscan`, `dnsrecon`, `dirb` |
| Web | `nikto`, `gobuster`, `ffuf`, `sqlmap`, `curl`, `wget` |
| Auth attacks | `hydra`, `crackmapexec` |
| SMB/AD | `smbclient`, `enum4linux`, `crackmapexec` |
| Password cracking | `john`, `hashcat` |
| Scripting | `python3`, `nc` |

---

## Troubleshooting**Step 2 — Start it if stopped (or Reset if error occurs):**
```bash
~/.openclaw/skills/prts-sandbox/scripts/sandbox-cmd.sh start
# CRITICAL RULE: If the start command fails with an error stating "the container name 'protocol-space-active' is already in use", you MUST run `reset`:
~/.openclaw/skills/prts-sandbox/scripts/sandbox-cmd.sh reset

| Problem | Fix |
|---------|-----|
| Commands fail / sandbox behaves oddly | Run `sandbox-cmd.sh reset` |
| API unreachable | Tell user: "Protocol Spaces API is offline" |
| Need a new tool installed | Ask user to install it — do NOT run `apt-get install` yourself |
| `start` returns error: "container name is already in use" | Run `sandbox-cmd.sh reset`, then verify `status` is true. |
| Commands fail / sandbox behaves oddly | Run `sandbox-cmd.sh reset` |
| API unreachable | Tell user: "Protocol Spaces API is offline" |
| Need a new tool installed | Ask user to install it — do NOT run `apt-get install` yourself |
---

## Quick reference

```bash
SANDBOX="~/.openclaw/skills/prts-sandbox/scripts/sandbox-cmd.sh"

$SANDBOX status          # Check if running
$SANDBOX start           # Start sandbox
$SANDBOX stop            # Stop sandbox
$SANDBOX reset           # Reset / fix broken sandbox
$SANDBOX exec <cmd>      # Run a command inside sandbox
```
