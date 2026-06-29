---
name: s7-tap
description: >-
  Read Siemens S7 PLCs and 仿西门子 国产 clones over S7comm (ISO-on-TCP / pyS7) —
  CPU info + run/stop, and read data blocks / merker / inputs / outputs (DB/M/I/Q)
  by area+type+offset or raw pyS7 address strings (DB1,REAL4 / M0.0 / MW10). A
  governed, MOC-gated write to a data block exists but is OFF by default. Use when
  the task names S7, S7-300/400/1200/1500, a DB/merker address, or rack/slot.
  Routes to the ot-aiops MCP server. For OPC-UA/Modbus/Mitsubishi/MTConnect/MQTT
  use the sibling *-tap skills; not for IT/network gear, Kubernetes, or backups.
---

# s7-tap

S7comm read-first telemetry via the **ot-aiops** MCP server, using **pyS7** (pure
Python, ISO-on-TCP / RFC1006 — no native libsnap7). Preview — validated against a
mocked client, NOT live PLCs. S7-300/400/1200/1500 and compatible clones.

## When to use
- A Siemens/仿西门子 PLC reachable over S7comm (`host:102`, `rack`/`slot`).
- Read DB/M/I/Q; check CPU run/stop.

## When NOT to use (routing)
- OPC-UA → `opcua-tap`; Modbus → `modbus-tap`; Mitsubishi → `mc-tap`; CNC →
  `mtconnect-tap`; MQTT/UNS → `sparkplug-tap`; cross-protocol triage →
  `industrial-diagnostics`. Rockwell/Allen-Bradley → not yet (`ethernetip_status`
  roadmap stub). IT/network/Kubernetes/hypervisor/backup → not this tool.

## Read tools

| Tool | Params | Returns |
|------|--------|---------|
| `s7_cpu_info` | `endpoint?` | `{cpu_status, cpu_info{module,serial,version}}` |
| `s7_read_area` | `area(DB\|M\|I\|Q), dtype, start, endpoint?, db=0, count=1, bit=0` | `{items:[{address,value}]}` |
| `s7_read_db` | `db, dtype, start, endpoint?, count=1` | `{items:[{address,value}]}` |
| `s7_read_many` | `addresses[] (pyS7 strings), endpoint?` | `{items:[{address,value}]}` |

`dtype` ∈ BIT, BYTE, WORD, INT, DWORD, DINT, REAL, LREAL, CHAR.
Example: `s7_read_db(db=1, dtype="REAL", start=4, count=2)` →
`{"items":[{"address":"DB1,REAL4","value":20.5}, ...]}`

## Write tool (HIGH risk · MOC · off by default)

`s7_write_db(db, dtype, start, value, endpoint?, dry_run=true)`
- **OT-DANGEROUS. 未经授权勿对生产控制系统写入.** Defaults to `dry_run=true`
  (preview only). Captures the BEFORE value and records an undo descriptor.
- To apply: set `dry_run=false` AND record an approver via
  `OPCUA_AUDIT_APPROVED_BY` (+ `OPCUA_AUDIT_RATIONALE`). CLI:
  `ot-aiops s7 write-db 1 INT 0 42 --apply` (double-confirm prompt).
- Dry-run returns `{dry_run:true, before, would_write, note}`; applied returns
  `{applied:true, before, written, _undo_id}`.

## Setup
`ot-aiops init` (s7: host/port/rack/slot) · `ot-aiops doctor` · `ot-aiops mcp`.
S7-1200/1500 default rack 0 / slot 1; S7-300/400 often rack 0 / slot 2. The CPU
must "Permit access with PUT/GET". 缺功能提 issue/PR 欢迎留言.
