# Operating vmware-debug with a local / small model

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
vmware-debug are specific to this skill.

vmware-debug exposes 14 MCP tools: 7 reads and 7 writes. It makes no VMware API calls
and needs no VMware account credentials — the calling agent gathers events from the other
skills, normalises them, and hands them over. The seven writes go to the local
investigation ledger under `~/.vmware/cases/`, never to a VMware system. That
makes it the safest skill in the family to point a small model at — and the one
most exposed to the model's reasoning, because its output *is* an
interpretation.

For a small model the ledger is more than bookkeeping: `grade_case` computes the
conclusion level from recorded evidence rather than accepting one, so a model
that would happily narrate "root cause confirmed" cannot record that unless the
evidence for it is actually in the folder.

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
| "Work read-only and never modify anything" | **The tool surface itself.** No tool reaches a VMware system. The seven [WRITE] tools write only to this skill's own local case ledger, so there is nothing in vSphere to withhold and nothing to switch off. |
| "Diagnose only — never apply the fix you propose" | **Structural.** This skill has no remediation tool or VMware API connection. Case tools update the local ledger and every tool writes a separate audit trail. Optional HTTPS serving uses caller tokens and TLS files. Remediation is routed to vmware-aiops or vmware-pilot by the calling agent. |
| "Do not fabricate a timeline — build it from the events I gave you" | **`build_incident_timeline` correlates only its input.** It is source-agnostic and has no way to fetch anything, so the timeline cannot contain an event the agent did not supply. |
| "Tell me when the symptom is outside what you can recognise" | **`list_symptom_categories`** states the catalogue, and unmatched symptoms come back as `uncategorized` rather than being forced into the nearest signature. |
| "Use explicit limits for queries that may return large amounts of data" | **The list envelope.** `list_symptom_categories` returns `{items, returned, limit, total, truncated, hint}` with `truncated` always `false` — which is the point: it states that the catalogue is complete instead of leaving you to infer it. |
| "Log everything you looked at" | **`~/.vmware/audit.db` and the case ledger.** Every debug tool call, a failed one included, writes one audit row (tool, time, user, agent, arguments, status and result — evidence `payload` and `events` are stored as `***`, and the results of `build_incident_timeline` and `record_case_timeline`, which quote event text, are not stored at all). Evidence submitted to a case is also recorded in the ledger with its source skill, tool, query and fetch time — so pass the real fetch time, never a placeholder. |

---

## The system prompt

Everything below still benefits from being stated explicitly. Copy this into
your agent's instruction block.

```text
## Tool use

- Gather real events with the companion skills' read tools before calling
  build_incident_timeline. Never answer from memory or assumption, and never
  hand-write events to represent what you believe happened.
- Never describe a tool call, and never output a JSON example, instead of
  executing the tool. If you intend to call a tool, call it.
- If a tool fails, report the actual error text. Do not complete the answer
  with assumptions about what the result would have been.
- Use explicit limits and time windows when gathering events. Do not request
  unlimited results unless the user asks for them.

## Skill routing

- vmware-debug: correlate pre-fetched events into a timeline, detect spikes,
  rank root-cause hypotheses, suggest next checks.
- Gather the events from: vmware-monitor (alarms, events, host logs),
  vmware-log-insight (centralised logs), vmware-aria (metrics, anomalies),
  vmware-nsx / vmware-nsx-security (network and firewall), vmware-storage.
- Route the fix to vmware-aiops, or to vmware-pilot when it needs approval
  gating. This skill executes nothing.

## Building the event set

- Every event needs ts (ISO-8601, epoch seconds, or millis), and the envelope
  shape {ts, source, severity, entity, text, fields}. An event that cannot be
  normalised is rejected by index — fix that event, do not drop the batch.
- Carry each event's original source and severity through unchanged. Do not
  re-grade a severity to make a story cohere.
- Pull from more than one source before concluding. A single source's view of
  an incident is not a correlation.
- Widen the window before concluding "no spike": spike detection needs at least
  three time bins, so a short window or a large bin_seconds can hide a burst.

## Data fidelity

- Never invent events, timestamps, entities, or relationships between them. If
  an event was not in the input, it does not exist for this answer.
- Preserve the exact severity and source values. Do not translate, normalise,
  or prettify them.
- Report the timeline in the order the tool returned it.
- If a requested field was not returned, show it as "not available".
- When a response is long, report every item it contains.
- Never record a secret. For an auth problem, record that a credential is
  missing, expired or rejected (the owning skill's `doctor` reports which) —
  never a password, token, or `.env` contents, in any evidence field. Do not
  open `.env` files to diagnose.

## Analysis discipline

- Separate observed data from interpretation. State which is which. In this
  skill that separation is the deliverable.
- Report the ranked hypotheses the tool returned, with its ranking. Do not
  promote your own preferred explanation above them, and do not present the
  top hypothesis as a diagnosis.
- Report next_checks as checks still to be run, not as findings.
- Do not claim a root cause is confirmed. The tool ranks; it does not conclude.
- Avoid generic recommendations that are not directly supported by the results.
```

---

## Known failure modes on small models

Observed with Llama 3.3 70B FP8 (Goose, on-prem H100), and useful as a
checklist when evaluating any local model against these skills:

| Symptom | Mitigation |
|---|---|
| Describes a tool call, or emits a JSON example, instead of executing it | The "never describe a tool call" rule above. This skill is unusually exposed to it: its input *is* JSON, so a model that has just been shown an event envelope will sometimes emit a fabricated one instead of gathering real events. Check that the events came from tool calls. |
| Long tool responses: omits items, or reports "no data returned" when data was present | Ask for explicit limits and narrow windows when gathering. `list_symptom_categories` states `truncated: false`, so a "no categories" claim is checkable against `returned`. |
| Adds generic recommendations unsupported by results | The "analysis discipline" rules. Root-cause output attracts invented advice more than any other shape of result in this family. |
| Drops requested fields or reorders results | State the required fields and ordering in the request itself. A reordered timeline is a different incident. |
| Multi-tool workflows take 30–50s end to end | Unavoidable in part — this skill's whole premise is a fan-out gather. Narrow each source's window before widening, and prefer the companion skills' aggregate tools when gathering. |
| Presents the top-ranked hypothesis as the confirmed cause | The "the tool ranks, it does not conclude" rule. |
| Re-grades an event's severity so the narrative fits | The "carry severity through unchanged" rule. |
| Concludes from one source because the others were slow to query | The "pull from more than one source" rule. |
| Reports "no spike" from a window too short to have a baseline | Three bins minimum. Widen the window or shrink `bin_seconds` before concluding. |
| Offers to apply the fix it proposed | It cannot. Route to vmware-aiops or vmware-pilot. |

## Reporting results

Local-model compatibility is an explicit design constraint for this family, and
the evidence base is small. If you evaluate a model against this skill —
Qwen, Mistral, Granite, or anything else — a report of what worked and what did
not is genuinely useful:
[github.com/vmware-skills/VMware-Debug/issues](https://github.com/vmware-skills/VMware-Debug/issues).
