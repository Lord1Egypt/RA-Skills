# Wazuh agent enrollment on a Windows Proxmox VM (via QGA)

Enroll a Windows VM into a Wazuh manager with **no AD creds, no GPO, no DC pivot** — scoped to exactly the target VM, executed as `NT AUTHORITY\SYSTEM` through the QEMU guest agent. Read `qga-exec.md` first; it's the execution layer this recipe rides on.

The Wazuh agent is passive — it reads and forwards logs; it opens no inbound ports and does not touch Active Directory. It is still a state-changing software install on a live server, so verify the target and change window before running it.

## What you need first

```jsonc
{
  "vmid":        0,                       // target Windows VM on Proxmox
  "managerIp":   "<manager-ip-on-vm-vlan>",   // the manager's address ON THE VM'S VLAN (not the mgmt IP)
  "agentName":   "<HOSTNAME>",            // what the agent registers as
  "group":       "<agent-group>",         // e.g. windows-crownjewels — create it before enrolling (step 1)
  "msiUrl":      "https://packages.wazuh.com/4.x/windows/wazuh-agent-<ver>.msi",
  "regPassword": "FROM YOUR VAULT — never hardcode. Pass over QGA stdin, not on the command line."
}
```

- **`managerIp` is VLAN-specific.** A multi-homed manager answers on a different address per VLAN; use the one reachable from the *guest's* network or enrollment silently fails to connect. Confirm from inside the guest if unsure (`cmd /c "ping -n 2 <managerIp>"`).
- The registration password is the manager's authd password. Keep it in the operator's secret manager and feed it to the guest over stdin (see `qga-exec.md` → "Passing the registration password"), never in the `msiexec` command line.

## Step 1 — Create the agent group on the manager (once, before enrolling)

**authd rejects an unknown group** at registration time (`ERROR: Invalid group: '<group>'`), and the agent never enrolls. Create it first, on the manager:

```bash
/var/ossec/bin/agent_groups -a -g <group> -q
```

This is the one manager-side prerequisite; everything else happens in-guest over QGA.

## Step 2 — Install the agent in-guest (download + silent install)

`curl.exe` is native on Server 2019+ (and Win10+); no PowerShell needed for the download. Run via QGA as SYSTEM:

```bat
curl.exe -sL -o C:\Windows\Temp\wz.msi <msiUrl>
msiexec /i C:\Windows\Temp\wz.msi /qn ^
  WAZUH_MANAGER=<managerIp> ^
  WAZUH_REGISTRATION_PASSWORD=<regPassword> ^
  WAZUH_AGENT_NAME=<agentName> ^
  WAZUH_AGENT_GROUP=<group>
```

- **Pass `WAZUH_REGISTRATION_PASSWORD` over stdin**, not on the command line — read it in a short PowerShell wrapper and build the `msiexec` argument list from it. See `qga-exec.md`.
- **`msiexec /qn` exit code: 0 or 3010 = success** (3010 = reboot required later). Anything else is a real failure — check `.data.exitcode` (REST) or `$LASTEXITCODE`. A silent install produces no stdout; verify by code.
- On Defender-heavy VMs run `cmd`/`msiexec` directly rather than wrapping in slow PowerShell; if you must reference the install dir in `cmd`, use the 8.3 path `C:\PROGRA~2\ossec-agent`.

**Alternative to the MSI registration password** (both worked 2026-06-28): install without `WAZUH_REGISTRATION_PASSWORD`, then drop the password into `C:\Program Files (x86)\ossec-agent\authd.pass` and restart. Useful when you'd rather not pass it as an MSI property at all.

## Step 3 — Connect (restart the service, usually twice)

The agent enrolls (fetches its key from authd) on **first service start**, but often reports `never_connected` until **one more restart** loads the key into the running process:

```bat
net stop WazuhSvc & net start WazuhSvc
```

Run it once to trigger enrollment, check the manager (step 4); if it's still `never_connected`, restart once more → `active`. (`&` chains the two `net` commands in `cmd`; both are instant.)

## Step 4 — Verify on the manager (the source of truth)

The agent's own logs can look healthy while the manager still rejects it — so **verify manager-side**:

- The agent shows `active` with the expected IP. The read-only `wazuh` monitoring skill's `wz.sh agents` command can answer this.
- If it's stuck `never_connected` / `disconnected`, the real reason is in **`/var/ossec/logs/ossec.log` on the manager** — authd lines show invalid-group, wrong password, or a key mismatch. Diagnose there, not in the guest.

## Hosts without a Proxmox guest agent

This skill is for Windows guests on Proxmox with QGA available. For physical Windows hosts, non-Proxmox hypervisors, Linux hosts, appliances, or syslog-only sources, use a Wazuh/endpoint-specific workflow instead of this Proxmox QGA workflow.

## Grounding

Confirm build-dependent Windows details against Microsoft documentation, especially `msiexec` exit codes (0/3010) and `cmd` chaining/operators.
