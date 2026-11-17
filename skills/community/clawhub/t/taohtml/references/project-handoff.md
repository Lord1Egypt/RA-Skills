# Project Handoff And Continuation

Use this reference whenever the request concerns an existing project, a handoff
record, a current HTML artifact, a review, or continued work. This is a task-intent
overlay on the three content routes in `intake-workflow.md`; it is not a fourth
content entry.

## Contents

- [Task Intent Overlay](#task-intent-overlay)
- [Source Role And Availability Map](#source-role-and-availability-map)
- [Structured Portable Handoff](#structured-portable-handoff)
- [Candidate Discovery Boundary](#candidate-discovery-boundary)
- [Read-Only Handoff](#read-only-handoff)
- [Continue Existing Work](#continue-existing-work)
- [Readiness And Operation Claims](#readiness-and-operation-claims)

## Task Intent Overlay

Record exactly one current task intent:

- `new_build`: create a new report through the ordinary route-aware workflow.
- `review_only`: read and map the handed-off state without changing files or
  producing HTML.
- `continue_existing`: take over an existing project and make an explicitly
  requested revision or continue production from its verified state.

Keep the content route separately as `idea_only | word_pdf |
existing_ppt_html`. A handoff can describe any of those routes, and an unresolved
route may remain unresolved during a read-only review. Do not show an extra entry
choice for “handoff.”

Infer the task intent from the user's requested action. Do not use filenames,
operating-system paths, company names, or a fixed keyword list to classify it. If
the user asks only to read, understand, audit, or take inventory, use `review_only`
even when they also say they may continue later. Move to `continue_existing` only
when they ask to change or resume the artifact.

## Source Role And Availability Map

For every bound item in a handoff, record these independent fields:

```text
source identity | source_binding | source_role | availability_status |
evidence_verification | inspection coverage | supports | limits |
observation basis
```

Use one of these source roles:

- `original_customer_material`: first-party material supplied by the customer,
  such as source documents, real data, screenshots, quotations, or evidence.
- `external_public_evidence`: a third-party or public source retrieved through the
  current task and recorded with its exact locator. It is source evidence, not
  customer material and not Agent-generated material.
- `secondary_handoff_summary`: an Agent- or human-written account of earlier work.
  It can orient the next Agent but does not replace the original material it
  describes.
- `current_artifact`: the current HTML, asset package, PDF export, or other report
  output. It proves what is presently rendered, not where its claims came from.
- `visual_reference`: a bound image or other supported reference used to define
  visual treatment or corporate fidelity.
- `agent_generated_material`: generated copy, simulated values, diagrams,
  placeholders, or other creative supplements.
- `described_unavailable_material`: material named or described in the handoff but
  not currently available for inspection.

Use one of these availability states:

- `workspace_readable`: the exact bound item can be opened in the current task
  workspace. Record `complete | partial` inspection coverage separately.
- `external_retrieved_inspected`: the exact external source was retrieved and
  inspected in the current session or connector, but is not represented as a
  workspace file. Record its locator, retrieval time, coverage, and claim check.
- `platform_visible_not_retrieved`: the platform shows the exact item, but its
  bytes have not been retrieved into the current task.
- `handoff_record_only`: the item exists only as a statement in a handoff record.
- `confirmed_missing`: the user or an authoritative platform/source state confirms
  that the exact item has been lost, deleted, or is no longer recoverable.
- `not_yet_verified`: current availability has not been established.

Record `evidence_verification` independently as `verified | unverified | conflicting
| not_applicable`. Availability proves access, not truth. Use `verified` only after
checking the exact external locator/content and the specific claim it supports;
record `conflicting` instead of silently choosing when sources disagree.

### Evidence Provenance Matrix

Treat this table as normative classification behavior:

| source_case | source_binding | source_role | availability_status | evidence_verification |
|---|---|---|---|---|
| `agent_retrieved_public_source_verified` | `agent_retrieved_external` | `external_public_evidence` | `external_retrieved_inspected` | `verified` |
| `agent_retrieved_public_source_unverified` | `agent_retrieved_external` | `external_public_evidence` | `external_retrieved_inspected` | `unverified` |

Use `agent_retrieved_external` only for a network or connector source retrieved
within the current authorized task. Record the exact URL or stable locator,
retrieval time, inspection coverage, supported claim, and verification result. This
binding never applies to a local candidate and never authorizes filesystem discovery.

Do not promote a role or status silently. A secondary summary remains secondary
even when it is detailed. A current artifact remains an artifact rather than
original evidence. A local file lookup that returns no match proves only that the
checked location did not produce the item; it does not prove that the material was
cleaned, deleted, or permanently lost. Keep the status `not_yet_verified` or
`handoff_record_only` until stronger evidence exists.

## Structured Portable Handoff

When the state must move across Agents or environments, read
`project-handoff-schema.md` and serialize it with
`project-handoff.schema.json`. Keep `workspace_ref`, stable project identity, and
the handoff snapshot identity separate. The handoff is a portable state export; it
is not a workspace database, enterprise asset repository, or complete project
source.

Run `scripts/validate_project_handoff.py` against the exact snapshot and portable
artifact root. Read its four conclusions independently: `schema_valid`,
`bindings_valid`, `continuation_ready`, and `delivery_ready`. A valid/openable
handoff is not delivery evidence. The validator verifies existing path/hash and
structured QA/authorization bindings only; it never claims to have executed
browser, asset, Runtime/editor, traceability, or delivery QA.

Use schema `1.0` unchanged for an existing legacy snapshot; do not add or infer a
Workflow Profile. New structured exports use `1.1` and always include
`current_build`: Direct HTML sets it to `null`, while a Report IR build binds the
current HTML artifact id, one hashed Build Manifest reference, and only the small
Workflow Profile identity summary. Keep full IR/Profile/Manifest content and
enterprise visual assets outside the handoff. Workflow Profile identity and
`design_binding.enterprise_profile` are separate contracts and never substitute for
one another.

Use only safe relative portable paths or stable non-local locators for identity.
Local absolute paths may appear solely as optional current-environment
observations. Unknown schema versions, extra fields, path escape, symlink traversal,
and current-file hash drift fail closed under the structured contract.

## Candidate Discovery Boundary

Apply the existing local/upload source-binding rules without exception. Inspect local
content only after the item is a current upload or explicit user selection, is
explicitly bound by the current task instruction, or is an exact candidate path the
user has confirmed. Keep `agent_retrieved_external` limited to external network or
connector evidence; never use it to bypass confirmation for a local file.

Candidate discovery is disabled by default. A selected route, workspace presence,
handoff scope, or current working directory does not authorize it. Only when the user
explicitly asks the Agent to find the source may discovery inspect metadata in a
narrow directory the user specified or clearly placed in scope. It may list precise
candidate paths for confirmation, but it must not read candidate content or auto-bind
even a single match. Do not recursively scan a home directory, Desktop, Downloads,
platform cache, cloud-sync root, unrelated workspaces, or other broad user locations
in search of a presumed source.

If a platform exposes an attachment or artifact that has not been retrieved, record
`platform_visible_not_retrieved` and use the platform's supported retrieval path.
Do not substitute a broad filesystem search. If retrieval is unavailable, report
the limitation without converting it to `confirmed_missing`.

## Read-Only Handoff

Default a `review_only` handoff to **0 clarification questions**. Read only eligible
bound items, build the role/availability map, and report:

1. what is directly available and inspected;
2. what is inherited only from a secondary account;
3. what the current artifact visibly contains;
4. what is platform-visible, record-only, confirmed missing, or not yet verified;
5. what work can safely continue; and
6. what would need source recovery or confirmation before a meaning-changing edit.

Do not restart the full route interview, create a Material Understanding Summary or
Report Design Brief merely for the audit, run formal production, or create/modify
HTML. If a missing item limits the review, state the limit and the smallest useful
next input without turning the read-only response into a question. Do not say that a
secondary handoff is “sufficient for all subsequent changes.”

The read-only result is a state map, not production authorization. It may say an
exact artifact was **found** or **can be previewed** when that is observed. It must
not say the report is **ready** or **formally deliverable**.

## Continue Existing Work

For `continue_existing`, reuse every still-supported fact from the role/availability
map and prior verified artifacts. Perform delta intake: do not replay startup,
audience, goal, length, visual, or structure questions whose answers remain known.
If one missing decision would materially change the requested result, ask only that
single largest gap and apply the existing repetition, information-gain, and six-
question limits in `intake-workflow.md`.

### Continuation Decision Matrix

Classify the requested delta before entering any gate. Treat this table as normative
workflow behavior:

| change_class | intake | material_summary | design_brief | required_current_validation |
|---|---|---|---|---|
| `meaning_preserving_local` | `do_not_rerun` | `do_not_rebuild` | `no_reconfirmation` | `exact_artifact_qa_and_delivery` |
| `meaning_changing` | `delta_only` | `rebuild_affected` | `confirm_complete_current_brief` | `authorization_qa_and_delivery` |

Use `meaning_preserving_local` only for an exact delivered artifact whose requested
change preserves its claims, real data, provenance, evidence relationships, core
viewpoint, structure, scope promise, and responsibility boundary. This path does not
reopen startup, intake, the Material Understanding Summary, or Report Design Brief
confirmation. Preserve the exact baseline identity, make the bounded change, and run
the applicable current asset, browser, Runtime/editor, traceability, and delivery
checks on the resulting artifact.

Use `meaning_changing` when the delta changes or could change source interpretation,
real data, attribution, evidence-to-claim relationships, real identities or achieved
outcomes, a core viewpoint or conclusion, chapter structure, scope promise, or
responsibility boundary. Rebuild only the affected source interpretation and brief
fields, then display and confirm the complete current brief through the existing gate
before formal production. If the class itself is genuinely ambiguous, ask only the
single largest scope-boundary question and count it under the existing six-question
limit.

Meaning-preserving continuation without restored original sources is normally safe
for:

- layout, spacing, typography, color, and other reversible visual adjustments;
- Runtime-compatible navigation, technical, portability, and local asset fixes; and
- local wording improvements that preserve the current claim, data, provenance,
  responsibility boundary, and conclusion.

Restore the original source or obtain explicit user confirmation of the exact change
before modifying:

- real data, quotations, citations, source attribution, or source status;
- which evidence supports which claim, and any uncertainty or contradiction;
- real customer/company identity or achieved outcomes; or
- a core viewpoint, main conclusion, scope promise, or responsibility boundary.

Explicit confirmation does not waive independent verification required for legal,
medical, financial, safety, or other high-risk facts. When an ordinary scene,
example, projected value, viewpoint, or expression is missing, continue under the
existing output-first rules, keep it separate from source facts, and add it to the
delivery-time `《待核实内容清单》`. Do not turn every unavailable original into a
block.

Previous gate artifacts and handoff claims may seed the current ledger, but they do
not by themselves prove current readiness. On `meaning_preserving_local`, do not
fabricate a new authorization state or force brief reconfirmation; verify the exact
baseline and resulting artifact through the applicable current QA and delivery
checks. On `meaning_changing`, satisfy the current-task contract in
`production-authorization.md` after the complete current brief is confirmed.

## Readiness And Operation Claims

Before claiming **ready** or **formally deliverable**, verify at least:

- the exact current artifact and every used material have eligible bindings, roles,
  availability states, and inspection coverage;
- the current production-authorization action succeeds when the selected path
  reopens formal production;
- strict offline asset QA and the required browser preflight/HTML QA pass on the
  current artifact;
- core-viewpoint/evidence traceability and any executable action path still match
  the confirmed brief, or on `meaning_preserving_local`, still match the exact
  delivered baseline without semantic drift; and
- the delivery verification handoff is current.

If these checks are incomplete, use bounded language such as **found**, **can be
previewed**, or **not yet verified**. Do not convert the existence of an HTML file,
a successful open, or a handoff assertion into **ready**, **QA passed**, or
**formally deliverable**.

Give operating instructions only from one of two evidence bases:

1. `current_artifact_tested`: exercise the controls on the exact current HTML and
   describe only what passed; or
2. `current_runtime_contract`: describe the generic behavior currently documented
   in `runtime-contract.md`, clearly stating when the handed-off artifact has not
   been verified to implement it.

Do not repeat an untested control description from a handoff summary. This overlay
does not add Runtime capabilities, bypass the content-editor boundary, create a new
corporate Profile data category, or weaken profile isolation and validation in
`profile-memory.md`.
