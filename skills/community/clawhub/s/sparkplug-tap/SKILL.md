---
name: sparkplug-tap
description: >-
  Consume MQTT / Sparkplug B / Unified Namespace (UNS) data — bounded plain-MQTT
  reads, Sparkplug B sample (topic parsed + payload decoded), edge-node/device
  discovery from NBIRTH/DBIRTH, and live topic-tree (UNS) browse. A governed,
  MOC-gated publish/command exists but is OFF by default. Use when the task names
  MQTT, Sparkplug, UNS, a broker, or an spBv1.0 topic. Routes to the ot-aiops MCP
  server. Consume-first. For OPC-UA/Modbus/Siemens/Mitsubishi/MTConnect use the
  sibling *-tap skills; not for IT/network gear, Kubernetes, hypervisors, or backups.
---

# sparkplug-tap

MQTT / Sparkplug B / UNS consume-first telemetry via the **ot-aiops** MCP server,
using **paho-mqtt** (pure Python). Preview — validated against synthetic protobuf
payloads, NOT a live broker. **Sparkplug B is fully decoded** (vendored Eclipse
Tahu protobuf schema, depends only on `protobuf`): per metric you get name,
**alias** (resolved via the BIRTH model), datatype (Int/Float/Bool/String/DateTime/
DataSet/Template…), value, timestamp, and `is_historical`/`is_null`. A
birth/death + seq model tracks node/device online state, applies NDATA/DDATA by
alias, and flags `seq` gaps; STATE topics surface primary-host status.

## When to use
- An MQTT broker / Sparkplug B edge / UNS (`host:1883` or `:8883` TLS, `topic`).
- Sample topics, discover edge nodes, browse the namespace tree.

## When NOT to use (routing)
- OPC-UA → `opcua-tap`; Modbus → `modbus-tap`; Siemens → `s7-tap`; Mitsubishi →
  `mc-tap`; CNC → `mtconnect-tap`; cross-protocol triage → `industrial-diagnostics`.
- IT/network/Kubernetes/hypervisor/backup → not this tool.

## Read/consume tools (bounded — never an open loop)

| Tool | Params | Returns |
|------|--------|---------|
| `mqtt_read_topic` | `endpoint?, topic="", count=25, timeout_s=10` | `{messages:[{topic,payload:{encoding,json\|text\|sparkplug_b}}]}` |
| `sparkplug_subscribe_sample` | `endpoint?, topic="", count=25, timeout_s=10` | `{historical_metric_count, seq_gap_count, samples:[{topic, sparkplug:{group_id,message_type,edge_node_id,device_id}, payload:{metrics:[{name,alias,datatype,value,is_historical}]}}]}` |
| `sparkplug_decode_payload` | `payload, encoding="base64", alias_map?` | `{seq, metric_count, historical_count, metrics:[{name,alias,datatype,value,timestamp,is_historical,is_null}]}` |
| `sparkplug_node_list` | `endpoint?, timeout_s=10, count=500` | `{nodes:[{group_id,edge_node_id,online,born,devices[...],metric_aliases_known,seq_gap_count}], primary_hosts:[{host_id,state}]}` |
| `uns_browse` | `endpoint?, topic="#", timeout_s=10, count=500` | `{topic_count, topics[...], tree{...}}` |

`sparkplug_decode_payload` decodes a single raw payload (base64 or hex) — useful to
inspect a captured NBIRTH/NDATA without a live broker; pass `alias_map` to resolve
alias-only NDATA/DDATA metrics to names.

Example: `sparkplug_node_list(endpoint="uns", timeout_s=15)` →
`{"node_count":2,"nodes":[{"group_id":"Plant1","edge_node_id":"Edge1","online":true,"born":true,"devices":["DevA"],"seq_gap_count":0}],"primary_hosts":[{"host_id":"primaryHost","state":"ONLINE"}]}`

## Command tool (HIGH risk · MOC · off by default)

`mqtt_publish(topic, payload, endpoint?, qos=0, retain=false, dry_run=true)`
- **OT-DANGEROUS. 未经授权勿对生产控制系统下发指令.** A command (e.g. Sparkplug
  NCMD/DCMD) can change a live system and has NO automatic inverse. Defaults to
  `dry_run=true`.
- Apply: `dry_run=false` + `OPCUA_AUDIT_APPROVED_BY`. CLI:
  `ot-aiops mqtt publish factory/cmd '{"sp":50}' --apply` (double-confirm prompt).

## Setup
`ot-aiops init` (mqtt: broker/port/topic/TLS/user) · `ot-aiops doctor` ·
`ot-aiops mcp`. Test against a local mosquitto broker (+ a Sparkplug edge). Full
Sparkplug B decode is bundled (no extra install). MQTT username/password is stored
encrypted; TLS optional. 缺功能提 issue/PR 欢迎留言.
