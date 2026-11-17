# Operating vmware-nsx-security with a local / small model

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
vmware-nsx-security are specific to this skill.

vmware-nsx-security exposes 22 MCP tools, 11 of which change state. This is a
firewall: a wrong rule does not raise an error, it silently permits or blocks
traffic, and nobody finds out until something breaks or nothing does.

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
| "Check whether a group is used anywhere before deleting it" | **`delete_group` scans** DFW and gateway-firewall rule sources, destinations, applied-to scope and policy scope, plus parent groups, and refuses when referenced. It also refuses when the scan itself fails, rather than assuming the group is unused. |
| "Do not delete a policy that still has rules in it" | **`delete_dfw_policy` refuses** while active rules exist. |
| "Show me what a delete would remove before it happens" | **The three delete tools preview by default.** Without `confirm=True` they return `blast_radius` and delete nothing; `confirm=True` is refused while a blocker remains or a read failed. Pass it only after the user has seen the preview. |
| "Use explicit limits for queries that may return large amounts of data" | **The list envelope.** `list_dfw_policies`, `list_dfw_rules`, `list_groups` and `list_idps_profiles` return `{items, returned, limit, total, truncated, hint}`, so the model reads truncation instead of guessing at it. A 50-row default page and a whole estate look identical without it. |
| "If a listing came back empty, say so rather than claiming the call failed" | Same envelope. Empty `items` with `truncated: false` means checked-and-none — a stated result, not a silence the model has to interpret. Note `total` is `null` for name-filtered and capped listings; `truncated: true` means `items` is not the whole collection and stays true on the last page, so page with `next_offset` and stop when it is `null`. |
| "Log every state change you make" | **The `@vmware_tool` decorator.** Every write is recorded to `~/.vmware/audit.db` before the model sees the result, and policy rules are evaluated ahead of execution. |
| "Block state-changing writes against a production target" | **Policy.** An opt-in environment-scoped `deny` rule in `~/.vmware/rules.yaml` matches a target's `environment:` label and refuses matching writes before execution. |

---

## The system prompt

Everything below still benefits from being stated explicitly. Copy this into
your agent's instruction block.

```text
## Tool use

- Always call an MCP tool before answering any question about the current NSX
  environment. Never answer from memory or assumption.
- Never describe a tool call, and never output a JSON example, instead of
  executing the tool. If you intend to call a tool, call it.
- If a tool fails, report the actual error text. Do not complete the answer
  with assumptions about what the result would have been.
- Use explicit limits on queries that may return large amounts of data. Do not
  request unlimited results unless the user asks for them.
- Every tool accepts an optional target. When more than one NSX Manager is
  configured, name the target explicitly rather than relying on the default.

## Skill routing

- vmware-nsx-security: DFW policies and rules, security groups, VM tags,
  IDS/IPS profiles and status, Traceflow.
- vmware-nsx: segments, Tier-0 and Tier-1 gateways, BGP, NAT, static routes,
  IP pools, transport nodes. Routing and switching are not this skill.
- vmware-monitor: read-only vCenter inventory, hosts, alarms, events.
- vmware-aiops: VM lifecycle.
- vmware-harden: compliance baselines and drift, including firewall posture.
- vmware-pilot: multi-step workflows that need approval gates.

## Data fidelity

- Never invent policies, rules, groups, tags, IP addresses or services. If a
  tool did not return it, it does not exist for this answer.
- Preserve the exact action, direction, disabled flag, category and sequence
  values the tools return. Do not translate, normalise, or prettify enum
  values, and never render ALLOW as "allowed" or DROP as "blocked".
- Report every rule field the user asked for, in the order returned. Rule
  evaluation is order-dependent, so a reordered list is a wrong answer.
- If a requested field was not returned, show it as "not available". Do not
  infer it from other fields.
- When a response is long, report every item it contains. If a result is
  truncated, the tool says so explicitly — report the truncation rather than
  describing the visible subset as the whole.

## Analysis discipline

- Separate observed data from interpretation. State which is which.
- Do not claim a security exposure unless the tool output contains explicit
  supporting evidence. An absent rule is not proof traffic is permitted; a
  zero hit count is not proof a rule is unused.
- Avoid generic recommendations that are not directly supported by the results.
- Never state that a change "will not affect existing traffic". You cannot
  know that from the tool output.

## Writes in vmware-nsx-security

- run_traceflow is a write: it injects a probe packet. Do not call it to
  "just check" something.
- Sequence number decides which rule matches first. State the sequence you are
  proposing and what it will sit before and after.
- Tag membership is matched as "scope|tag", and multiple criteria are ORed.
  Read get_group before assuming what a group contains.
- remove_vm_tag can change dynamic group membership, and therefore which rules
  apply to a VM. Say so before proposing it.
- get_group returns at most 50 effective members. member_count is the group's
  real size, and members.truncated says whether the sample withheld any — read
  those two rather than counting members.items.
```

---

## Known failure modes on small models

Observed with Llama 3.3 70B FP8 (Goose, on-prem H100), and useful as a
checklist when evaluating any local model against these skills:

| Symptom | Mitigation |
|---|---|
| Describes a tool call, or emits a JSON example, instead of executing it | The "never describe a tool call" rule above. Also check your harness is not echoing tool schemas into context — models imitate the nearest format they see. |
| Long tool responses: omits items, or reports "no data returned" when data was present | Ask for explicit limits so responses stay small. Check the envelope's `truncated` / `returned` / `total` fields rather than trusting the model's summary — a "no data" claim is checkable against `returned`. A dropped rule in a firewall listing is a security answer that is quietly wrong. |
| Adds generic recommendations unsupported by results | The "analysis discipline" rules. Firewall output attracts invented advice ("consider tightening this rule") more than anything else in the family. |
| Drops requested fields or reorders results | State the required fields and ordering in the request itself. Rule order is semantic here, not cosmetic. |
| Multi-tool workflows take 30–50s end to end | `get_dfw_policy` and `get_group` each answer a whole question in one call. Fetch the policy once and read its rules from that result rather than looping. |
| Calls `run_traceflow` believing it to be a read | The rule above. Its name suggests a query; its effect is an injected packet. |
| Reads a zero hit count as "this rule is unused" and proposes deleting it | The "zero hit count is not proof" rule. A new rule has zero hits by construction. |
| Summarises ALLOW/DROP into prose and inverts the meaning | The "never render ALLOW as allowed" rule. Keep the enum verbatim. |
| Retries a refused deletion, or works around it by deleting the references first | The refusals are guards. Report the reason and let a human decide. |

## Reporting results

Local-model compatibility is an explicit design constraint for this family, and
the evidence base is small. If you evaluate a model against this skill —
Qwen, Mistral, Granite, or anything else — a report of what worked and what did
not is genuinely useful:
[github.com/vmware-skills/VMware-NSX-Security/issues](https://github.com/vmware-skills/VMware-NSX-Security/issues).
