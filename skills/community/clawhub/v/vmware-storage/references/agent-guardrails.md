# Operating vmware-storage with a local / small model

Claude-class models drive this skill without special instruction. Smaller and
locally-hosted models — Llama 3.3 70B, Qwen, Mistral, and similar, served
through Goose, Ollama, or OpenShift AI — need explicit operating rules to call
tools reliably.

This page exists because an operator wrote those rules by hand first. The
guardrails below are adapted, with thanks, from the working configuration
[@juanpf-ha](https://github.com/juanpf-ha) developed while running
vmware-monitor and vmware-aria against a production vSphere estate with Llama
3.3 70B FP8 on an on-prem H100
([VMware-AIops#31](https://github.com/vmware-skills/VMware-AIops/issues/31)). The
cross-skill rules are identical across this family; the parts below marked
vmware-storage are specific to this skill.

vmware-storage exposes 16 MCP tools, 4 of which change state. The write
surface is small but sharp: removing an iSCSI send target can make LUNs — and
every VM living on them — inaccessible.

> **Disclaimer**: This is a community-maintained open-source project and is
> **not affiliated with, endorsed by, or sponsored by VMware, Inc. or Broadcom
> Inc.** "VMware" and "vSphere" are trademarks of Broadcom.

---

## First: the rules you no longer need to write

Several guardrails from the original configuration are now enforced by the
skill itself. Prompt instructions are advisory — a model can ignore them.
These are structural, so it cannot.

| Guardrail you would otherwise prompt for | Now enforced by |
|---|---|
| "Preview the change before applying it" | **`confirm` defaults to false.** A call to any of the 4 write tools without `confirm: true` changes nothing and returns `blast_radius`. Previewing is the default path, not a convention the model has to remember to honour. |
| "Don't cut off storage that is in use" | **Refusal.** `remove_iscsi_target` with `confirm: true` is refused when a datastore would lose every path, or when any path or static target behind the send target cannot be attributed. |
| "Use explicit limits for queries that may return large amounts of data" | **The list envelope.** The four datastore read tools return `{items, returned, limit, total, truncated, hint}`, so the model reads truncation instead of guessing at it. All four enumerate their collection in full, so `total` is the real count and `truncated` is always `false`. |
| "If a listing came back empty, say so rather than claiming the call failed" | Same envelope. Empty `items` with `truncated: false` means checked-and-none — a stated result, not a silence the model has to interpret. |
| "Log every state change you make" | **The `@vmware_tool` decorator.** Every operation is recorded to `~/.vmware/audit.db` before the model sees the result, and policy rules are evaluated ahead of execution. `remove_iscsi_target` is classified `risk:high` and goes through the policy confirmation gate. |

---

## The system prompt

Everything below still benefits from being stated explicitly. Copy this into
your agent's instruction block.

```text
## Tool use

- Always call an MCP tool before answering any question about the current
  VMware environment. Never answer from memory or assumption.
- Never describe a tool call, and never output a JSON example, instead of
  executing the tool. If you intend to call a tool, call it.
- If a tool fails, report the actual error text. Do not complete the answer
  with assumptions about what the result would have been.
- Use explicit limits on queries that may return large amounts of data. Do not
  request unlimited results unless the user asks for them.
- Datastore and host names are case-sensitive. Resolve the exact name with a
  list tool before using it; do not correct or reformat what the user typed.

## Skill routing

- vmware-storage: datastores, datastore browsing, image scanning, iSCSI
  adapters and send targets, vSAN health and capacity, and read-only Fibre
  Channel HBA inventory and multipath path state.
- vmware-monitor: read-only vCenter inventory, hosts, alarms, events,
  performance. Prefer it for any question that only reads.
- vmware-aiops: VM lifecycle. This skill cannot power, create, delete or
  reconfigure a VM — route those there.
- vmware-vks: Supervisor storage policies and namespace storage usage.
- vmware-aria: capacity forecasting and trend analysis.
- vmware-pilot: multi-step workflows that need approval gates.

## Data fidelity

- Never invent datastores, hosts, LUNs, targets, or capacity figures. If a tool
  did not return it, it does not exist for this answer.
- Preserve the exact status, health-state and accessibility values the tools
  return. Do not translate, normalise, or prettify enum values.
- Report capacity in the units the tool returned. Do not convert GB to TB or
  recompute a usage percentage yourself.
- If a requested field was not returned, show it as "not available". Do not
  infer it from other fields.
- Preserve the original order and the full set of fields when the user asks
  for specific ones.
- When a response is long, report every item it contains. If a result is
  truncated, the tool says so explicitly — report the truncation rather than
  describing the visible subset as the whole.

## Analysis discipline

- Separate observed data from interpretation. State which is which.
- Do not claim a capacity, performance, or configuration problem unless the
  tool output contains explicit supporting evidence. A datastore at 80% is a
  number, not an incident.
- Avoid generic recommendations that are not directly supported by the results.

## Writes in vmware-storage

- Call any iSCSI or rescan tool without confirm first, show the user the
  returned blast_radius, and pass confirm: true only after they decide.
- remove_iscsi_target is destructive: LUNs behind that target can become
  inaccessible, taking their VMs with them. Say so before proposing it.
- "Already enabled" from enable_iscsi is not an error. Report the
  returned HBA device and IQN.
- After adding a target, the storage subsystem needs 10-30 seconds before new
  LUNs appear. An empty rescan result is not proof the target is wrong.
```

---

## Known failure modes on small models

Observed with Llama 3.3 70B FP8 (Goose, on-prem H100), and useful as a
checklist when evaluating any local model against these skills:

| Symptom | Mitigation |
|---|---|
| Describes a tool call, or emits a JSON example, instead of executing it | The "never describe a tool call" rule above. Also check your harness is not echoing tool schemas into context — models imitate the nearest format they see. |
| Long tool responses: omits items, or reports "no data returned" when data was present | Ask for explicit limits so responses stay small. Check the envelope's `truncated` / `returned` / `total` fields rather than trusting the model's summary — a "no data" claim is checkable against `returned`. |
| Adds generic recommendations unsupported by results | The "analysis discipline" rules. Capacity output invites invented advice more than most — hold it to the evidence. |
| Drops requested fields or reorders results | State the required fields and ordering in the request itself, not only in the system prompt. |
| Multi-tool workflows take 30–50s end to end | Prefer the tools that answer in one call: `list_all_datastores` already carries capacity, usage % and VM count, and `get_vsan_health` covers cluster health and disk groups together. Neither needs a per-object follow-up loop. |
| Silently corrects a datastore name's case and reports on the wrong object | Resolve names through `list_all_datastores` first, and have the model echo the resolved name before acting. |
| Recomputes usage percentages and gets them wrong | The "report capacity in the units the tool returned" rule. |
| Treats "already enabled" as a failure and retries | It is a stated result. The response carries the HBA device and IQN. |
| Reports a host as "missing the LUN" when that host was never read | `list_storage_device_paths` lists such hosts in `hosts_not_read` and sets `complete: false`; they are never in `not_seen_on`, and neither is any disk that lives inside one host. Require the model to name unread hosts as unknown. |
| Calls a `standby` path a failure | Only `states_needing_attention` (dead/disabled) is a finding. `standby` is normal on active/passive arrays. |

## Reporting results

Local-model compatibility is an explicit design constraint for this family, and
the evidence base is small. If you evaluate a model against this skill —
Qwen, Mistral, Granite, or anything else — a report of what worked and what did
not is genuinely useful:
[github.com/vmware-skills/VMware-Storage/issues](https://github.com/vmware-skills/VMware-Storage/issues).
