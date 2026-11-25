# `vms` and `lxc` are SEPARATE enumerations — a fleet-wide claim needs both

Proxmox has two guest types and two command families. Using one and reporting on "the fleet"
under-reports, silently:

| | LXC container | Virtual machine |
|---|---|---|
| List | `pve.sh lxc <node>` · `pct list` | `pve.sh vms` · `qm list` |
| **Run a command inside** | **`pct exec <vmid> -- <cmd>`** | **`qm guest exec <vmid> -- <cmd>`** |
| Recovery backdoor | `pct exec` always works | **none** — snapshot before risky changes |

`qm guest exec` needs `agent: 1` in the VM config plus `qemu-guest-agent` running, and returns JSON
(read `out-data`, and note it ends `",` when other fields follow). `pct list` puts status in field 2
while `qm list` puts it in field 3 — reusing the same `awk` across both silently returns nothing.

**Real cost of getting this wrong:** an audit script built on `pct list` alone reported "34 of 34"
hosts compliant while omitting every VM — behind which sat a host with 108 pending updates and four
hosts still accepting SSH passwords. **State coverage as a denominator you verified, never as "all".**
