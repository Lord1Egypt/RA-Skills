---
name: proxmox-wazuh-enroll
description: >-
  Install and enroll the Wazuh agent inside Windows VMs hosted on Proxmox VE
  using QEMU guest agent execution (qm guest exec or Proxmox REST API), with no
  WinRM, SSH, RDP, GPO, or AD credentials required. Use this skill whenever the
  user asks to get a Windows Proxmox guest, domain controller, file server, or
  group of Windows VMs reporting to Wazuh; install, push, roll out, onboard, or
  enroll the Wazuh agent; fix a just-enrolled Windows Proxmox VM stuck at
  never_connected; or keep registration secrets off command lines while deploying
  via guest agent. This skill performs active in-guest deployment and verification
  against the Wazuh manager. Do not use for read-only Wazuh dashboard, CVE, alert,
  or coverage checks; Linux, LXC, appliance, or syslog enrollment; generic Proxmox
  VM creation; generic PowerShell guest exec; or non-Wazuh endpoint agents.
metadata:
  openclaw:
    homepage: https://github.com/eddygk/proxmox-wazuh-enroll
    os:
      - linux
    requires:
      bins:
        - bash
---

# Proxmox → Windows Wazuh Enrollment

Install the Wazuh agent inside a Windows VM hosted on Proxmox VE, driven through the QEMU guest agent (QGA) as `NT AUTHORITY\SYSTEM`. No AD credentials, no GPO, no domain-controller pivot — scoped to exactly the target VM. This is a state-changing install on a live server; confirm the target VM, manager address, agent group, and registration-secret handling before running it.

## Execution layer (read first)

`references/qga-exec.md` is how every step runs in the guest: `qm guest exec` on the Proxmox host (preferred — blocks and returns output) or the Proxmox REST API off-host, with the registration password passed over **stdin** and never on a command line. Skim it before the recipe.

## The recipe, at a glance

Full detail — including the env block to fill and the `authd.pass` alternative — is in `references/wazuh-agent-enroll.md`. The shape:

1. **Create the agent group on the manager first.** authd rejects an unknown group (`ERROR: Invalid group`) and the agent never enrolls: `/var/ossec/bin/agent_groups -a -g <group> -q`.
2. **Install in-guest via QGA:** `curl.exe` download → `msiexec /qn` with `WAZUH_MANAGER` (the manager's address **on the VM's VLAN**), `WAZUH_AGENT_NAME`, `WAZUH_AGENT_GROUP`, and the registration password over **stdin**. Success = `msiexec` exit **0 or 3010**.
3. **Connect:** `net stop WazuhSvc & net start WazuhSvc` — enrolls on first start (may show `never_connected`); one more restart makes it `active`.
4. **Verify on the manager** (the source of truth): the agent shows `active`; diagnose failures in `/var/ossec/logs/ossec.log` on the manager, not in the guest.

## Secrets

The registration password comes from the operator's vault and is fed to the guest over QGA stdin (`--pass-stdin` / REST `input-data`). Keep it off command lines, out of logs, and out of chat — see `references/qga-exec.md`.

## When this is NOT the skill

- **Querying Wazuh** (which agents are up, CVEs, alerts, coverage) → the read-only `wazuh` monitoring skill. This skill *installs*; it doesn't report.
- **Linux or appliance agents** (Ubuntu, pfSense/OPNsense, TrueNAS) → those enroll host-side over 1514/1515 or via syslog, not Windows-guest QGA.
- **Provisioning the VM itself** (create/clone/boot a Windows VM on Proxmox) → a Proxmox ops skill.

## Reference files

- `references/qga-exec.md` — the QGA execution layer: on-host `qm guest exec` vs off-host REST, secrets over stdin, `cmd` vs PowerShell + 8.3 paths, silent-installer exit codes, the unescaped-control-char parsing gotcha.
- `references/wazuh-agent-enroll.md` — the full enrollment recipe: create the group, install via MSI over QGA, connect, verify manager-side; the `authd.pass` alternative; out-of-scope host guidance.
