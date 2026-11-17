# Structured Project Handoff

Use this reference when exporting, importing, or validating a TaoHtml project
handoff. Read `project-handoff.md` first for the workflow meaning of task intent,
source roles, availability, evidence verification, and change classes. This file
defines their strict portable serialization; it does not replace that workflow.

## Contents

- [Contract Files](#contract-files)
- [Identity Boundaries](#identity-boundaries)
- [Snapshot Shape](#snapshot-shape)
- [Source And Decision Bindings](#source-and-decision-bindings)
- [Design And Artifact Bindings](#design-and-artifact-bindings)
- [Recorded QA And Authorization](#recorded-qa-and-authorization)
- [Four Independent Conclusions](#four-independent-conclusions)
- [Portability And Path Safety](#portability-and-path-safety)
- [Version Policy](#version-policy)
- [Future Boundaries](#future-boundaries)

## Contract Files

- `project-handoff.schema.json`: normative JSON Schema, current version `1.1`;
  the exact original `1.0` shape remains accepted.
- `../scripts/validate_project_handoff.py`: deterministic structural, binding,
  continuation, and delivery evaluator.

Run:

```bash
python scripts/validate_project_handoff.py \
  --handoff <snapshot.json> \
  --artifact-root <portable-project-root> \
  --require bindings_valid
```

Choose `schema_valid`, `bindings_valid`, `continuation_ready`, or
`delivery_ready` with `--require`. Exit `0` means only the requested layer is
true. Exit `1` means the document is structurally valid but that layer is false.
Exit `2` means the JSON or schema contract is invalid. Always inspect all four
reported booleans and their separate `blocking_reasons`.

The CLI accepts strict JSON only. Duplicate object keys and Python-style
non-finite values (`NaN`, `Infinity`, and `-Infinity`) fail before schema
evaluation. This prevents parser-dependent replacement or numeric behavior from
changing a handoff's meaning.

## Identity Boundaries

Keep three identities independent:

| Object | Purpose | Must not become |
|---|---|---|
| `workspace_ref` | Portable, opaque reference to the workspace context | A local absolute path or an enterprise asset repository |
| `project_identity` | Stable project id, identity version, and project reference | A company-name, filename, session, or platform heuristic |
| `handoff_snapshot` | Identity and creation metadata for this exported state | The complete project source or the project identity itself |

The validator computes `handoff_sha256` from the snapshot bytes. Lineage records
the parent snapshot hash separately; a document never embeds and recursively
hashes itself.

`workspace_ref.observation.local_absolute_path` is optional current-environment
observation only. It never acts as the workspace identity, a portable artifact
locator, or a readiness input. Put no local absolute path in `project_ref`, source
identity, artifact locator, design binding, or future opaque reference.

## Snapshot Shape

Every top-level object is closed: missing fields and additional fields fail
`schema_valid`. Required sections are:

| Section | Contract |
|---|---|
| `schema_version` | Exact supported handoff version |
| `workspace_ref` | Portable workspace reference plus optional local observation |
| `project_identity` | Stable project identity independent of workspace and snapshot |
| `handoff_snapshot` | Export id, creation time, exporter version |
| `task` | `task_intent`, `content_route`, `change_class`, and structured `requested_delta` |
| `source_ledger` | Exact source identity/binding, role, availability, verification, coverage, supports, limits, and observation basis |
| `decisions` | Still-valid decisions, automatic inferences, and unresolved items |
| `confirmations` | Independent VI, design-brief, and production-authorization records |
| `design_binding` | Exactly one built-in, project-theme, enterprise-profile, or unresolved binding |
| `artifacts` | Current, delivered-baseline, previous, supporting, and gate-record artifacts |
| `qa_records` | Existing structured QA records bound to an artifact id and hash |
| `current_build` | In `1.1`, `null` for Direct HTML or the small Report IR Build Manifest/Profile identity record |
| `lineage` | Parent handoff, exact baseline, previous artifacts, and current delta |
| `audit_metadata` | Optional platform/model/cost audit information, never readiness input |

All arrays and nullable fields remain present. Use empty arrays or `null`; do not
omit a field or add a case-specific extension.

`requested_delta` records affected source and decision ids, whether meaning is
preserved, and the interpretation basis. A meaning-changing delta has at least one
affected source or affected decision. `source_reinspection` requires every listed
affected source—not merely one of them—to be readable/retrieved, inspected
original customer material or external public evidence. A pure chapter-structure,
scope, or responsibility-boundary change may instead use
`affected_decision_ids + explicit_user_confirmation` without inventing an affected
source. `both` requires both the source conditions and the exact confirmation.
A meaning-preserving delta uses `interpretation_basis=not_applicable`; it must not
manufacture a new source interpretation or brief confirmation.

## Source And Decision Bindings

Copy the exact Task 1 source-binding, role, availability, and
evidence-verification enums from the schema. Availability and evidence truth are
orthogonal. For example,
`external_retrieved_inspected + unverified` is valid and must stay unverified.

`supports` is intentionally structured. Its `support_kind` prevents provenance
promotion:

| Source role | Allowed support kind |
|---|---|
| Original customer material or external public evidence | `source_fact` |
| Secondary handoff summary | `orientation_only` |
| Current artifact | `rendered_state` |
| Visual reference | `visual_fact` |
| Agent-generated material | `generated_content` |
| Described unavailable material | `availability_description` |

A secondary summary that declares `source_fact` support therefore fails
`bindings_valid` even though its JSON shape is valid. A current artifact can prove
what is rendered, not the provenance or truth of the rendered claim.

Every `workspace_readable` source uses a safe relative `portable_path` with a
lowercase SHA-256 and `complete | partial` inspection coverage. The validator
checks the current bytes. `agent_retrieved_external` remains limited to an exact
`stable_external_locator` classified as
`external_public_evidence + external_retrieved_inspected`; no local candidate can
use that binding.

Decision ids are unique across `still_valid`, `inferred`, and `unresolved`.
Source and decision references must resolve inside the snapshot. Each unresolved
item states independently whether it blocks continuation or delivery.

## Design And Artifact Bindings

`design_binding.kind` selects exactly one binding:

- `built_in_theme`: one of the four shipped theme ids, plus its manifest version
  and current `theme.json` hash. The validator compares it with the installed
  TaoHtml asset.
- `project_theme`: artifact id, theme version, and theme hash. The referenced
  artifact must have kind `project_theme`; its version and the current primary
  HTML's `versions.theme_version` must both equal the selected binding version.
- `enterprise_profile`: task-local profile-use binding path, profile id, immutable
  integer profile version, theme fingerprint, and binding hash. The validator
  reads the existing `profile_store.py bind` JSON, checks its closed field set and
  essential scalar structure, and compares profile id/version/theme fingerprint
  with the handoff declaration. It does not load or copy the enterprise assets.
  The current HTML has no existing profile-version encoding that is comparable to
  this record, so the validator does not invent one; readiness relies on the
  verified profile-use binding instead.
- `unresolved`: all three binding payloads stay `null`.

Each artifact records:

- stable `artifact_id`, kind, role, availability, locator, and SHA-256;
- `baseline_identity` when it descends from an exact delivered baseline;
- Runtime, editor, theme, and optional compiler versions; and
- optional `report_ir_ref` with its own hash; it stays opaque in `1.0` and is
  cross-checked only when a `1.1 current_build` declares a Report IR build.

TaoHtml's primary report source is HTML. Exactly the `current` and
`delivered_baseline` roles identify primary report artifacts, so either role must
have `kind=html`; those two roles are therefore type-compatible. ZIP and PDF are
supporting/export artifacts, never primary current/baseline truth. Attachments,
design briefs, VI boards, project themes, authorization records, and QA records are
also ineligible for either primary role. A current artifact and a delivered
baseline are separate roles even when their bytes happen to match. The current
HTML's baseline identity must agree with `lineage`.

In a `1.0` snapshot, `compiler_version` and `report_ir_ref` retain their original
opaque-reference semantics. The validator never infers a Workflow Profile for that
version.

Version `1.1` adds `current_build` at the top level because it describes the identity
of the current build rather than enterprise visual state. Direct HTML records set it
to `null`; they do not gain a Report IR requirement or a new customer question. A
Report IR build records only:

- `artifact_ref`, pointing to the one current HTML artifact whose locator/hash and
  `compiler_version` remain authoritative in `artifacts`;
- `build_manifest_ref`, containing the portable Manifest locator and file SHA-256;
  and
- `workflow_profile`, containing only `binding_state`, `primary_profile_id`,
  `definition_version`, and `binding_sha256`.

The handoff does not copy the Manifest, Report IR, Profile definition,
`selection_basis`, overlays, report content, or enterprise assets. When the current
HTML, normalized IR, and Build Manifest are local hashed portable files, the
validator cross-checks their refs/hashes, Compiler version, IR version and canonical
hash, and the deterministic Manifest/Profile binding. A `1.0` IR must remain
`legacy_unbound` with null Profile identity; a `1.1` IR must be `bound`. Any mismatch
fails `bindings_valid`. The validator does not call the Compiler, run the Report IR
Validator, reinterpret Profile semantics, or execute QA.

`current_build.workflow_profile` is independent of
`design_binding.enterprise_profile`: the former binds a workflow contract to the
IR/build identity, while the latter binds enterprise visual assets. Neither field
may substitute for, populate, or validate the other.

For continuation or delivery through an enterprise profile, export only the small
profile-use binding record as a hashed `portable_path`; keep the enterprise assets
at their profile reference. The portable check deliberately does not call the full
profile store or require that store to exist in a read-only receiving environment.
A non-local stable profile locator remains useful state, but it is not
continuation-ready until the exact binding JSON is local, hash-current, structurally
valid, and matches declared profile id/version/theme fingerprint. Production
readiness fails closed on any mismatch.

## Recorded QA And Authorization

VI confirmation, Report Design Brief confirmation, and production authorization
are three independent records. `status`, `scope`, artifact id/hash, and trace are
never inferred from each other.

A current meaning-changing continuation requires:

1. affected sources or decisions and interpretation basis recorded in
   `requested_delta`;
2. the complete current design brief confirmed with
   `scope=current_snapshot`, whose exact `design_brief` artifact is
   `workspace_readable` and hash-current; and
3. a separate current production-authorization record bound to the current
   primary HTML id/hash and confirmed brief hash.

`new_build` uses the same local current-brief and exact-current authorization gates
before it can claim continuation or delivery readiness. A recorded confirmation
whose artifact is only platform-visible, handoff-only, missing, or not yet verified
remains useful state but cannot satisfy either production path.

For both `new_build` and `meaning_changing`, continuation additionally requires
`formal-html` in that verified exact-current authorization. Delivery requires
`formal-html + browser-qa + deliver-formal-html` together in the same record. The
three actions are independent formal boundaries; any non-empty subset is not a
substitute for the missing action.

When `design_binding.kind=project_theme`, VI remains independent. Its exact
`vi_board` artifact must be local and hash-current for production readiness; new
builds and meaning-changing work additionally require `scope=current_snapshot`.
An inherited locally verified VI may remain valid for a meaning-preserving local
change. A VI confirmation never substitutes for the design brief or production
authorization.

A meaning-preserving local continuation binds the exact delivered baseline and
current artifact but does not require or create a current brief confirmation or
production authorization. An inherited confirmed brief may remain recorded with
`scope=inherited_baseline`; it is context, not a reopened gate.

An executed QA entry uses a `qa_record` artifact containing an exact JSON object:

```json
{
  "schema_version": "1.0",
  "record_id": "...",
  "check_type": "browser_qa",
  "status": "passed",
  "artifact_ref": "current-html",
  "artifact_sha256": "...",
  "executed_at": "...",
  "tool": "..."
}
```

The handoff binds both the QA record file hash and the subject artifact hash. The
validator reads that existing structured record and compares the binding. It does
not launch a browser, inspect rendering, rerun asset QA, or decide whether the QA
tool was competent. Its output therefore always states
`qa_execution_claim=not_executed_by_validator`.

An authorized production record is similarly strict and contains only:
`schema_version`, `record_type`, `status`, target artifact id/hash, confirmed brief
hash, and `authorized_actions`. For `new_build` and `meaning_changing`, both the
handoff authorization and the structured authorization file must target the exact
current primary HTML id and current hash; targeting a known baseline or supporting
artifact fails closed. A file that merely exists or opens does not satisfy either
record contract. An otherwise exact authorization without `formal-html` cannot
make a new-build or meaning-changing snapshot continuation-ready; delivery requires
all three formal actions in the same verified record.

## Four Independent Conclusions

| Layer | Meaning | Explicit non-meaning |
|---|---|---|
| `schema_valid` | JSON shape, exact fields, enums, scalar constraints, and supported schema version pass | No file, hash, provenance, or readiness claim |
| `bindings_valid` | References, role/support semantics, safe local paths, current hashes, lineage, confirmations, recorded QA/authorization, and any declared current-build identity are coherent | No claim that an incomplete workflow can continue or deliver |
| `continuation_ready` | The requested task branch has the minimum state needed for safe continuation | No claim that current QA or delivery passed |
| `delivery_ready` | A non-review task has a hash-current artifact, applicable gates, no delivery blocker, and passed structured asset/browser/Runtime-editor/traceability/delivery records bound to that artifact | No claim that this validator executed those checks |

The evaluator applies these branch rules:

- Any non-null `1.1 current_build` must have its current HTML, normalized IR, and
  Build Manifest locally hash-verified before it can contribute to
  `continuation_ready` or `delivery_ready`. A stable locator or handoff-only current
  artifact may preserve useful identity state, but cannot impersonate local build
  verification.

- `review_only`: may be schema-valid, bindings-valid, and continuation-ready with
  missing originals and unresolved content route. It is always
  `delivery_ready=false`.
- `meaning_preserving_local`: continuation requires one hash-current delivered
  baseline, one hash-current current artifact, matching lineage/baseline identity,
  and no continuation blocker. It never reopens brief confirmation. Delivery also
  requires every applicable current QA/delivery record.
- `meaning_changing`: continuation additionally requires affected
  source or decision scope, its declared interpretation evidence, local
  hash-current complete brief, resolved design binding, and current formal
  production authorization bound to the exact current HTML. Only then can current
  QA records contribute to delivery readiness.
- `new_build`: may be recorded as a valid preproduction state, but it is not
  continuation-ready until route, local hash-current current HTML and brief,
  resolved design, and exact-current formal authorization are present. Delivery
  additionally requires all current QA/delivery records.

`audit_metadata.platform`, `model`, `cost`, and `notes` are excluded from every
readiness calculation. Changing only those values changes the snapshot hash, not
the four readiness results.

## Portability And Path Safety

Use `/`-separated relative paths below `--artifact-root`. Reject absolute paths,
Windows drive paths, `..`, empty/dot segments, backslashes, and duplicate
separators. For every readable local binding, reject a symlink at the target or in
any parent component, resolve the path, require it to remain below the exact root,
require a regular file, and compare its current SHA-256.

Use `stable_locator` for a portable non-local artifact reference and
`stable_external_locator` for retrieved public evidence. The validator does not
retrieve either one, so a non-local current artifact cannot become continuation or
delivery ready until its exact bytes are locally bound and checked.

## Version Policy

Versions `1.0` and `1.1` are accepted with explicit, closed shapes:

- `1.0` is the original contract. It forbids `current_build`, keeps Report IR and
  Compiler fields opaque, and never receives a guessed Profile value.
- `1.1` requires the `current_build` field. Direct HTML uses `null`; a Report IR
  current artifact requires the small build/Profile binding described above.

Unknown versions fail `schema_valid`. A `1.0` snapshot is not silently upgraded,
and a `1.1` field cannot be smuggled into `1.0`; there is no implicit downgrade,
permissive extra-field mode, or best-effort migration. A future migration must be
an explicit tool that produces a new snapshot and preserves the old snapshot hash
in lineage.

## Future Boundaries

This contract reserves clean references for TaoHtml Workspace, TaoHtml Project,
Report IR, and Compiler work. It does not implement those systems inside the handoff
validator:

- `workspace_ref` is opaque; it is not a workspace database or asset store.
- `project_identity` is identity only; it is not a mutable Project service.
- `report_ir_ref` never embeds a Report IR payload. Under `1.1 current_build`, the
  validator reads only the local normalized IR identity/Profile fields needed for
  deterministic cross-checking; it does not execute the full Report IR workflow.
- `compiler_version` records provenance only; the validator does not compile.
- `build_manifest_ref` binds one existing Manifest file; it never copies the
  Manifest or turns the handoff into a build database.
- `enterprise_profile` references immutable profile state and never copies the
  enterprise asset collection into the handoff.

Keep future implementations behind these references instead of expanding the
handoff into an enterprise repository or a second project source of truth.
