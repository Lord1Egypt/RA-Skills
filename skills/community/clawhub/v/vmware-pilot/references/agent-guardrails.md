# Operating vmware-pilot with a local / small model

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
vmware-pilot are specific to this skill.

vmware-pilot is the odd one out. It manages no infrastructure of its own — it
designs multi-step workflows, tracks their state, and gates them on human
approval. Two consequences follow, and both matter more on a small model than
on a large one: **authoring a workflow is itself the write operation**, and
**by default pilot executes nothing** — the calling agent does. (Started with
`--dispatch`, pilot runs each step itself in that skill's own MCP server; the
result then has no `pending_dispatch`, and you do not perform the steps.)

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
| "Do not execute steps yourself — hand them back for a human to run" | **The dispatch contract.** Without `--dispatch`, pilot never calls a companion skill's MCP tools; it returns a step description and the calling agent invokes the tool. With `--dispatch`, pilot runs the steps and stops at each approval gate, so nothing after a gate runs before `approve`. |
| "Check the plan makes sense before running it" | **`review_workflow`** performs a structural sanity check and returns `approved` or `needs_revision`. It is a read tool that inspects a definition without executing it. |
| "Put an approval gate before anything destructive" | **Custom-workflow rejection.** In a custom workflow (YAML, `create_workflow`, or a draft), a destructive or unclassifiable step — or any step passing `confirm: True` — with no `require_approval` before it makes `create_workflow` / `confirm_draft` / `create_workflow_from_template` refuse to save it and `run_workflow` refuse to run it — `force=True` does not override that. The refusal names the step and the gate to insert. |
| "Log every state change you make" | **The `@vmware_tool` decorator.** Every workflow transition is recorded to `~/.vmware/audit.db`, and `get_workflow_status` returns the state plus its audit log. |

The one guardrail this skill does not hand you: pilot's list tools return bare
collections, not the family `{items, returned, limit, total, truncated, hint}`
envelope. Truncation is not self-declaring here.

---

## The system prompt

Everything below still benefits from being stated explicitly. Copy this into
your agent's instruction block.

```text
## Tool use

- Always call an MCP tool before answering any question about workflow state.
  Never answer from memory or assumption.
- Never describe a tool call, and never output a JSON example, instead of
  executing the tool. If you intend to call a tool, call it.
- If a tool fails, report the actual error text. Do not complete the answer
  with assumptions about what the result would have been.
- Use explicit limits on queries that may return large amounts of data. Do not
  request unlimited results unless the user asks for them.

## Skill routing

- vmware-pilot: multi-step workflows — design, plan, run, approve, roll back,
  cancel, and inspect state.
- vmware-aiops: VM lifecycle. Without `--dispatch` pilot never calls it; you
  do, when pilot hands you a step.
- vmware-monitor: read-only vCenter inventory, hosts, alarms, events.
- vmware-nsx / vmware-nsx-security: networking and firewall.
- vmware-storage, vmware-vks, vmware-aria, vmware-avi: their own domains.
- A single-step request does not need a workflow. Call the skill directly.

## The dispatch contract

- Read the result: a `pending_dispatch` list means pilot runs without
  `--dispatch` and YOU invoke each listed tool. No `pending_dispatch` means pilot
  ran the steps itself — do not run them again.
- Never claim a step ran because pilot advanced its state. State advanced
  because you told pilot it did.
- If you cannot invoke the tool a step names — it is not installed or is
  otherwise unavailable — say so and stop. Do not improvise a substitute.

## Designing workflows

- A step's tool must be a real tool on the named skill. get_skill_catalog is a
  curated design aid, not a whitelist: it lists a hand-picked subset, so a tool
  missing from the catalog may still exist. Confirm against the target skill's
  own SKILL.md before writing a step that names it.
- Never invent a tool name to make a step read well. A workflow that names a
  tool which does not exist fails at run time, several steps in.
- Order steps by dependency, not by narration. Gather state before changing it;
  put the approval gate before the first irreversible step, not after it.
- Give every reversible step a rollback_tool and rollback_params. A step with
  no rollback cannot be undone by the rollback tool.
- Nothing is ever rolled back automatically. After a failure, ask the user
  before undoing anything. On the MCP server the rollback tool cannot see the
  steps you performed (they stay not_executed), so undo them yourself: call each
  one's rollback_tool with its rollback_params, last step first.
- issue_tkc_kubeconfig and issue_supervisor_kubeconfig return a live credential.
  Only fetch one when the user asks, write it to a file, and never print the
  token.
- Run review_workflow before executing. Treat needs_revision as a stop.

## Data fidelity

- Never invent workflows, steps, templates, or state transitions. If a tool did
  not return it, it does not exist for this answer.
- Preserve the exact workflow and step state values the tools return. Do not
  translate, normalise, or prettify them.
- Report the steps in their defined order. Order is semantic in a workflow.
- If a requested field was not returned, show it as "not available".
- When a response is long, report every item it contains.

## Analysis discipline

- Separate observed data from interpretation. State which is which.
- Do not claim a workflow succeeded, or that an estate is now in some state,
  on the basis of workflow state alone. Verify with the owning skill's read
  tools.
- Avoid generic recommendations that are not directly supported by the results.
```

---

## Known failure modes on small models

Observed with Llama 3.3 70B FP8 (Goose, on-prem H100), and useful as a
checklist when evaluating any local model against these skills:

| Symptom | Mitigation |
|---|---|
| Describes a tool call, or emits a JSON example, instead of executing it | The "never describe a tool call" rule above. Also check your harness is not echoing tool schemas into context — models imitate the nearest format they see. |
| Long tool responses: omits items, or reports "no data returned" when data was present | Ask for explicit limits so responses stay small. Pilot's lists have no truncation envelope, so verify long results rather than trusting the summary. |
| Adds generic recommendations unsupported by results | The "analysis discipline" rules. |
| Drops requested fields or reorders results | State the required fields and ordering in the request itself. In a workflow, reordering the steps changes what the plan does. |
| Multi-tool workflows take 30–50s end to end | Start from a built-in template with `create_workflow_from_template` rather than designing from scratch; `get_workflow_status` returns state and audit log together. |

### Workflow design failures — the pattern to watch here

Designing a plan is generative work, and it is where a small model's habits do
the most damage. These are specific to this skill:

| Symptom | Mitigation |
|---|---|
| Writes a step naming a tool that does not exist — a plausible name assembled from the skill's naming pattern rather than its actual surface | The "never invent a tool name" rule. `get_skill_catalog` lists a curated subset, so absence from the catalog is not proof a tool is missing — and presence of a *plausible* name in the model's head is no proof it exists. Confirm against the target skill's SKILL.md. Nothing catches this until run time. |
| Orders steps by narrative rather than dependency: changes state before gathering it, or verifies before acting | The "order by dependency" rule, then `review_workflow`. |
| Places the approval gate after the irreversible step it was meant to guard | Refused structurally for destructive and unclassifiable steps (see the table above); for medium-risk writes, the "order by dependency" rule. State explicitly which step the gate protects. |
| Omits `rollback_tool` on reversible steps, leaving nothing for `rollback` to undo | The rollback rule above. Add it while writing the step, not afterwards. |
| Treats pilot's state machine as evidence the infrastructure changed | The dispatch contract. Pilot records what you told it; verify with the owning skill. |
| Reports a step as done without having invoked the companion tool | Same. This is the dispatch contract's characteristic failure. |
| Designs a workflow for something that is a single tool call | The routing rule. A workflow is overhead unless there is an approval gate or a real dependency chain. |

## Reporting results

Local-model compatibility is an explicit design constraint for this family, and
the evidence base is small. If you evaluate a model against this skill —
Qwen, Mistral, Granite, or anything else — a report of what worked and what did
not is genuinely useful:
[github.com/vmware-skills/VMware-Pilot/issues](https://github.com/vmware-skills/VMware-Pilot/issues).
