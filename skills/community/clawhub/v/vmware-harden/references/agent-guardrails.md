# Operating vmware-harden with a local / small model

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
vmware-harden are specific to this skill.

vmware-harden exposes 8 MCP tools and every one of them is a read. The risk
here is not a destructive call — there is none to make. It is that compliance
output is exactly the shape of text a small model likes to embellish, and an
invented violation, or an invented clean bill of health, is a costly answer.

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
| "Only ever read — never modify the estate" | **The tool surface.** All 6 tools carry the `[READ]` marker and none modify vSphere or NSX — there is no write tool here to withhold in the first place. |
| "Never remediate anything you find — only report it" | **Structural.** This skill has no remediation tool. `get_remediation` returns a *suggestion*; execution is deferred to vmware-pilot behind an approval gate. A model cannot apply a fix from here even if asked to. |
| "Do not modify the systems you are auditing" | **`scan_target` is read-only against vSphere and NSX.** The rows it writes go only to the local DuckDB twin — a cache of its own observations, not managed infrastructure. |
| "Use explicit limits for queries that may return large amounts of data" | **The list envelope.** `list_baselines`, `get_baseline_rules` and `list_drift_events` return `{items, returned, limit, total, truncated, hint}`. Because the twin is local, `total` is a real count: a page that exactly fills `limit` is still reported `truncated: false` when it is genuinely the whole set. `list_violations` keeps its own older `{violations, total, limit, offset, has_more}` envelope with the same guarantee. |
| "If a listing came back empty, say so rather than claiming the call failed" | Same envelope. Empty `items` with `truncated: false` means checked-and-none — a stated result, not a silence the model has to interpret. In a compliance context that distinction is the whole answer. |
| "Log everything you looked at" | **The `@vmware_tool` decorator.** Every call is recorded to `~/.vmware/audit.db`, reads included. |

---

## The system prompt

Everything below still benefits from being stated explicitly. Copy this into
your agent's instruction block.

```text
## Tool use

- Always call an MCP tool before answering any question about compliance
  posture. Never answer from memory, from training data about CIS or 等保
  content, or from assumption.
- Never describe a tool call, and never output a JSON example, instead of
  executing the tool. If you intend to call a tool, call it.
- If a tool fails, report the actual error text. Do not complete the answer
  with assumptions about what the result would have been.
- Use explicit limits on queries that may return large amounts of data. Do not
  request unlimited results unless the user asks for them.
- Compliance findings come from a scan of this estate. A scan must have run
  before you can report on it.

## Skill routing

- vmware-harden: compliance baselines (CIS, vSphere SCG, 等保 2.0, PCI-DSS),
  violations, drift events, remediation suggestions, scans.
- vmware-pilot: actually applying a remediation, behind an approval gate.
  This skill cannot execute a fix.
- vmware-aiops: VM and host reconfiguration.
- vmware-nsx-security: DFW rules and security groups.
- vmware-monitor: read-only vCenter inventory, hosts, alarms, events.

## Data fidelity

- Never invent violations, rules, severities, control identifiers, or framework
  references. If a tool did not return it, it does not exist for this answer.
- Preserve the exact severity, status and rule identifier values the tools
  return. Do not translate, normalise, or prettify them, and do not map a
  control to a different framework's numbering.
- A rule that could not be evaluated is not a pass. Report it in its own
  category. The tools return this as `coverage.undetermined` (with
  `coverage.undetermined_rules` naming each rule and the attribute that blocks
  it) — a rule whose data no collector gathers is not executed at all, so its
  result is unknown, not compliant.
- **An empty violation list is not a compliance verdict.** Before saying an
  estate is compliant or clean, check `coverage.complete`. When it is false,
  state how many rules were evaluated out of how many. When `coverage.tracked`
  is false the snapshot predates coverage tracking, so its coverage is unknown —
  ask for a re-scan rather than assume.
- If a requested field was not returned, show it as "not available". Do not
  infer it from other fields.
- Preserve the original order and the full set of fields when the user asks
  for specific ones.
- When a response is long, report every item it contains. If a result is
  truncated, the tool says so explicitly — report the truncation rather than
  describing the visible subset as the whole. Never summarise a violation list
  down to "the important ones" unless asked.

## Analysis discipline

- Separate observed data from interpretation. State which is which.
- Do not state that the estate is compliant. Report which rules passed, which
  failed, and which produced no evidence, and let the reader conclude.
- Do not claim a finding is exploitable, or assign it a business impact, unless
  the tool output says so.
- Avoid generic hardening advice that is not directly supported by the results.

## Remediation suggestions

- get_remediation returns a suggestion, never an applied change. Present it as
  a proposal.
- When ANTHROPIC_API_KEY is not configured the advisor returns a deterministic
  mock template. Say so rather than presenting boilerplate as analysis.
- Route execution to vmware-pilot. Do not attempt the change through another
  skill's tools on your own initiative.
```

---

## Known failure modes on small models

Observed with Llama 3.3 70B FP8 (Goose, on-prem H100), and useful as a
checklist when evaluating any local model against these skills:

| Symptom | Mitigation |
|---|---|
| Describes a tool call, or emits a JSON example, instead of executing it | The "never describe a tool call" rule above. Also check your harness is not echoing tool schemas into context — models imitate the nearest format they see. |
| Long tool responses: omits items, or reports "no data returned" when data was present | Ask for explicit limits so responses stay small. Check the envelope's `truncated` / `returned` / `total` fields rather than trusting the model's summary — a dropped violation is a compliance report that is quietly wrong. |
| Adds generic recommendations unsupported by results | The "analysis discipline" rules. This is the dominant failure here: a model that has read a lot of hardening guides will happily produce advice the scan never justified. |
| Drops requested fields or reorders results | State the required fields and ordering in the request itself, not only in the system prompt. |
| Multi-tool workflows take 30–50s end to end | `list_violations` already carries severity and can be filtered server-side — filter there rather than pulling everything and reasoning over it. |
| Recites CIS or 等保 control text from training data instead of the scanned baseline | The "never answer from training data" rule. Have the model quote the rule identifier the tool returned. |
| Reports "no violations" when no scan has run, or when the twin DB is empty | Require the model to state the scan it is reporting on. An empty twin is not a clean estate. |
| Counts unevaluated rules as passes and overstates the compliance rate | The "could not be evaluated is not a pass" rule. Such rules appear in `coverage.undetermined`, not in `violations`; a scan where `coverage.complete` is false has not judged the whole baseline. |
| Presents the mock remediation template as LLM-generated analysis | The `ANTHROPIC_API_KEY` rule above. |
| Offers to apply the fix | It cannot. Route to vmware-pilot. |

## Reporting results

Local-model compatibility is an explicit design constraint for this family, and
the evidence base is small. If you evaluate a model against this skill —
Qwen, Mistral, Granite, or anything else — a report of what worked and what did
not is genuinely useful:
[github.com/vmware-skills/VMware-Harden/issues](https://github.com/vmware-skills/VMware-Harden/issues).
