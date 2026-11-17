# Operating vmware-aria with a local / small model

Claude-class models drive this skill without special instruction. Smaller and
locally-hosted models — Llama 3.3 70B, Qwen, Mistral, and similar, served
through Goose, Ollama, or OpenShift AI — need explicit operating rules to call
tools reliably.

This page covers what goes wrong most often with vmware-aria specifically:
**alert-to-resource correlation**. For the full cross-skill guardrail set, the
complete system prompt, and the small-model failure-mode checklist, see the
canonical guide in
[vmware-monitor's references](https://github.com/vmware-skills/VMware-Monitor/blob/main/skills/vmware-monitor/references/agent-guardrails.md).

These guardrails are adapted, with thanks, from the working configuration
[@juanpf-ha](https://github.com/juanpf-ha) developed while running vmware-aria
and vmware-monitor against a production vSphere estate
([VMware-AIops#31](https://github.com/vmware-skills/VMware-AIops/issues/31)).

> **Disclaimer**: This is a community-maintained open-source project and is
> **not affiliated with, endorsed by, or sponsored by VMware, Inc. or Broadcom
> Inc.** "VMware" and "vSphere" are trademarks of Broadcom.

---

## 1. Alert-to-resource correlation

This is the sequence small models get wrong most reliably. An Aria alert does
not carry the affected object's name — only a `resourceId`. Correlating an
alert with vCenter therefore means: fetch the alert, read its `resourceId`,
fetch that resource, confirm its name and kind, then query vmware-monitor. Two
UUIDs are in play, and they get swapped.

**Use `investigate_alert` instead of chaining the steps by hand.** It performs
the whole sequence server-side and returns:

- `alert` — Aria's own criticality / status / impact / control-state values,
  passed through verbatim.
- `resource` — the affected object, or `null`.
- `correlation` — both UUIDs **explicitly labelled** (`alert_id` vs
  `resource_id`), plus `resource_name`, `resource_kind`, and a `confirmed`
  flag. Every key is always present; unresolved values are explicit `null`.
- `next_step` — the exact vmware-monitor tool and argument to call next, or
  `null` when there is nothing confirmed to hand off. For an "Objects are not
  receiving data from adapter instance" alert it is vmware-aria's own
  `list_resources` with `collection_status=NO_DATA_RECEIVING`, which names the
  objects that stopped reporting.
- `warnings` — why anything above is incomplete; empty on success.

A resource that cannot be resolved degrades to a warning plus explicit nulls
rather than an error, so the alert you already fetched is never lost.

If you must drive the steps manually, state these rules explicitly:

```text
- Use investigate_alert to go from an alert to its affected resource.
- Do not pass an alert UUID where a resource UUID is expected. They are
  different objects; investigate_alert labels both.
- Only query vCenter for a resource once correlation.confirmed is true.
  The next_step block names the exact tool and argument to use.
```

---

## 2. Aria-specific data fidelity

Aria's enum values carry operational meaning and must survive the model
untouched:

```text
- Preserve the exact criticality (INFORMATION / WARNING / IMMEDIATE /
  CRITICAL), status, impact, and control-state values the tools return.
  Do not translate, normalise, or prettify them.
- alertLevel is the criticality field. An alert definition has no top-level
  criticality — it is the maximum severity across its states.
- Recommendations hang off the alert definition, not the alert.
- Do not claim a capacity, performance, or risk problem unless the tool output
  contains explicit supporting evidence. Badge colour alone is not a diagnosis.
```

---

## Reporting results

Local-model compatibility is an explicit design constraint for this family, and
the evidence base is small. If you evaluate a model against this skill, a
report of what worked and what did not is genuinely useful:
[github.com/vmware-skills/VMware-Aria/issues](https://github.com/vmware-skills/VMware-Aria/issues).
