# Operating vmware-avi with a local / small model

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
vmware-avi are specific to this skill.

vmware-avi exposes 28 MCP tools, 6 of which change state. It straddles two
control planes — the AVI Controller and a Kubernetes cluster running AKO — and
most of the trouble a small model gets into here comes from confusing which
side of that boundary an object lives on.

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
| "Log every state change you make" | **The `@vmware_tool` decorator.** Every write is recorded to `~/.vmware/audit.db` before the model sees the result, and policy rules are evaluated ahead of execution. |
| "Convert time windows into the units the API expects" | **The ops layer does the conversion.** Analytics duration accepts either an integer of seconds or a shorthand suffix (`30m`, `24h`, `7d`); the model does not have to know the controller wants seconds. |
| "Use the controller's IP, not its hostname" | **The connection layer resolves it.** Some analytics endpoints reject a hostname; the FQDN is resolved to an address before the SDK sees it. |

Note the one guardrail this skill does **not** hand you: vmware-avi's list tools
return bare collections, not the family `{items, returned, limit, total,
truncated, hint}` envelope. Truncation is therefore not self-declaring here, so
the "report every item" and "state the limit you used" rules below carry more
weight than they do in the rest of the family.

---

## The system prompt

Everything below still benefits from being stated explicitly. Copy this into
your agent's instruction block.

```text
## Tool use

- Always call an MCP tool before answering any question about the current AVI
  or AKO environment. Never answer from memory or assumption.
- Never describe a tool call, and never output a JSON example, instead of
  executing the tool. If you intend to call a tool, call it.
- If a tool fails, report the actual error text. Do not complete the answer
  with assumptions about what the result would have been.
- Use explicit limits and time windows on queries that may return large amounts
  of data. State the window you used in the answer.
- Analytics windows accept an integer of seconds or a shorthand suffix such as
  30m, 24h or 7d. Pick one and say which.

## Skill routing

- vmware-avi: virtual services, pools and pool members, SSL certificates,
  Service Engines, VS analytics and error logs, AKO pod/config/sync/ingress
  diagnostics, multi-cluster and AMKO.
- vmware-nsx: segments, gateways, NAT, routing. The underlay is not this skill.
- vmware-nsx-security: DFW rules and security groups.
- vmware-vks: Supervisor and Tanzu Kubernetes cluster lifecycle.
- vmware-monitor: read-only vCenter inventory, hosts, alarms, events.
- vmware-aiops: VM lifecycle.
- vmware-pilot: multi-step workflows that need approval gates.

## Data fidelity

- Never invent virtual services, pools, members, certificates or Service
  Engines. If a tool did not return it, it does not exist for this answer.
- Preserve the exact operational state, health-score and enabled/disabled
  values the tools return. Do not translate, normalise, or prettify them.
- Report metric values and their units exactly as returned. Do not rescale,
  average, or recompute a percentage yourself.
- If a requested field was not returned, show it as "not available". Do not
  infer it from other fields.
- Preserve the original order and the full set of fields when the user asks
  for specific ones.
- These tools return bare lists, not a truncation envelope. If you applied a
  limit, say so in the answer; never present a limited result as the whole set.

## Analysis discipline

- Separate observed data from interpretation. State which is which.
- Do not claim a performance, certificate or capacity problem unless the tool
  output contains explicit supporting evidence.
- An empty analytics series means no data was recorded for that window — it is
  not evidence of zero traffic, and not evidence of an outage.
- Avoid generic recommendations that are not directly supported by the results.

## Two control planes

- Controller-side objects (virtual services, pools, SEs, certificates) and
  Kubernetes-side objects (AKO pod, Helm values, Ingress) are different things.
  Name which side you are reporting on.
- An Ingress with no virtual service is an AKO reconciliation question, not a
  missing-VS question. Use check_ako_ingress, then get_ako_logs, then
  diff_ako_sync — in that order.
- SSL certificates are tenant-scoped. An empty certificate list may mean the
  configured user cannot see that tenant, not that no certificates exist.

## Writes in vmware-avi

- set_virtual_service_enabled takes a virtual service out of service. Call it without confirm
  first: that returns blast_radius (the VS, its current state, the pools and
  members behind it) and changes nothing. Show it and wait for the user's
  decision before calling again with confirm=true.
- upgrade_ako_config is a Helm release upgrade against a live cluster. Show
  diff_ako_config first, then the preview (without confirm) of the upgrade.
- A pool member that reports "down" straight after being enabled is failing its
  health monitor. Report that, do not re-enable it in a loop.
```

---

## Known failure modes on small models

Observed with Llama 3.3 70B FP8 (Goose, on-prem H100), and useful as a
checklist when evaluating any local model against these skills:

| Symptom | Mitigation |
|---|---|
| Describes a tool call, or emits a JSON example, instead of executing it | The "never describe a tool call" rule above. Also check your harness is not echoing tool schemas into context — models imitate the nearest format they see. |
| Long tool responses: omits items, or reports "no data returned" when data was present | Ask for explicit limits and narrow time windows so responses stay small. This skill has no truncation envelope to check the model's summary against, so verify against the controller when the answer matters. |
| Adds generic recommendations unsupported by results | The "analysis discipline" rules. |
| Drops requested fields or reorders results | State the required fields and ordering in the request itself, not only in the system prompt. |
| Multi-tool workflows take 30–50s end to end | Prefer the tools that answer a whole question in one call: `diagnose_ako_ingress` replaces a check/logs/diff sequence, and `check_ssl_cert_expiry` replaces enumerating certificates and comparing dates by hand. |
| Reads an empty analytics series as an outage | The "empty series means no data" rule. Virtual services with no traffic legitimately return nothing for the window. |
| Passes a bare number where a duration was meant, or invents its own unit | State the window explicitly, in seconds or with a suffix. |
| Confuses an AKO problem with a Controller problem and reports the wrong root cause | The "two control planes" block above. Make the model name the side it is describing. |
| Reads an empty SSL certificate list as "no certificates configured" | Certificates are tenant-scoped. Report it as a visibility result, not an inventory result. |

## Reporting results

Local-model compatibility is an explicit design constraint for this family, and
the evidence base is small. If you evaluate a model against this skill —
Qwen, Mistral, Granite, or anything else — a report of what worked and what did
not is genuinely useful:
[github.com/vmware-skills/VMware-AVI/issues](https://github.com/vmware-skills/VMware-AVI/issues).
