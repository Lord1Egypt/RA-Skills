# Production Authorization

Use this fail-closed state contract for the current invocation. It separates
confirmation previews from formal HTML production and delivery. A previous task's
confirmation, an existing HTML file, or the user's initial request to “continue” does
not authorize the current formal output.

## Current-Task State

Before any preview gate or formal production action, write a task-local JSON file that
uses this exact shape:

```json
{
  "schema_version": "1.3",
  "task_id": "current-invocation-id",
  "route": "word_pdf",
  "visual_route": "built_in",
  "material_summary": {
    "status": "confirmed",
    "artifact_path": "gates/material-summary.md",
    "artifact_sha256": "9b41e9e597cd42bd247366d8435fc48eff12d24a818677eaf82c68c2a4ec8fbb",
    "confirmation_ref": "current conversation turn reference"
  },
  "reference_vi": {
    "status": "not_required",
    "artifact_path": null,
    "artifact_sha256": null,
    "confirmation_ref": null
  },
  "profile_use": {
    "status": "not_required",
    "artifact_path": null,
    "artifact_sha256": null
  },
  "project_theme_compiled": false,
  "built_in_theme": {
    "theme_id": "rigorous-consulting-report",
    "selection_status": "user_selected",
    "decision_ref": "current conversation theme-choice reference"
  },
  "motion_density": {
    "density": "moderate",
    "selection_status": "delegated_to_taohtml",
    "decision_ref": "current conversation motion-delegation reference"
  },
  "design_brief": {
    "status": "pending",
    "artifact_path": "gates/report-design-brief.md",
    "artifact_sha256": null,
    "confirmation_ref": null,
    "design_decisions_sha256": null
  }
}
```

Use `idea_only | word_pdf | existing_ppt_html` for `route` and
`unresolved | built_in | static_reference | profile_reuse` for `visual_route`. Word/PDF and existing
PPT/HTML routes require a current confirmed material summary; idea-only uses
`material_summary.status` = `not_required`. Static reference requires a current confirmed VI and a compiled
project theme; other visual routes use `reference_vi.status` = `not_required` and
`project_theme_compiled` = `false`, except that `profile_reuse` requires the existing
validated project theme and therefore uses `true`.

`built_in_theme.selection_status` is `pending | user_selected |
delegated_to_taohtml` on `built_in`; it is `not_required` with null `theme_id` and
`decision_ref` on `unresolved | static_reference | profile_reuse`. A decided built-in
route requires one exact current catalog id and an auditable current-conversation
decision reference. `motion_density.selection_status` is `pending | user_selected |
delegated_to_taohtml` for every visual route and uses only the Report IR native
`minimal | moderate | rich` values. A recommendation alone is still `pending`.

These two choices are independent from the ordinary six-question clarification
budget. Reaching the cap or three no-gain rounds cannot change either status. When one
choice is already decided, preserve it and request only the remaining pending choice.
Static-reference and Profile reuse never require a competing built-in theme, but they
still require a customer-selected or explicitly delegated motion density.

For `profile_reuse`, use `reference_vi.status: not_required` and set `profile_use` to
`pending` until `profile_store.py bind` writes the current task-local binding. Then set
`profile_use.status: bound`, record its safe relative path and exact current SHA-256,
and rerun the checker. The checker validates the binding against the live TaoHtml home,
active profile/version, VI/reference hashes, and the existing project-theme loader. A
reusable binding cannot accompany another visual route. A `temporary_override` binding
may accompany the replacement built-in/static-reference route but cannot authorize
`profile_reuse`.

Schema v1.1 and v1.2 states remain readable only for fail-closed migration. The checker
synthesizes pending design choices, discards any legacy brief-confirmation authority,
and reports `migration.required: true`; such a state cannot authorize formal HTML.
Migrate by creating a strict v1.3 state, recording the applicable decisions and exact
references, updating the customer-readable brief with those decisions, and confirming
that complete current brief again. V1.1 also receives legacy
`profile_use=not_required`; it cannot express profile reuse. Never add placeholder
decisions merely to preserve an old authorized result.

A v1.3 state uses the exact current shape above. A previously drafted v1.3 confirmed
brief without `design_decisions_sha256` is invalid rather than implicitly trusted:
reset that brief gate to pending, obtain `current_design_decisions_sha256` through the
normal checker result, update the brief, and confirm it again.

Before requesting confirmation, save every
applicable material summary, VI board, or design brief as a customer-readable file
inside the current task artifact root. A `confirmed` gate records its safe relative
`artifact_path`, the SHA-256 of those exact current bytes, and the current conversation
`confirmation_ref`. Recompute and record the digest only when that exact file is the
artifact the user confirmed. A later byte change invalidates the gate until the changed
artifact is confirmed again.

A confirmed `design_brief` additionally records `design_decisions_sha256`, the checker
helper's canonical SHA-256 over the complete normalized `built_in_theme` and
`motion_density` objects. This binds every theme id/density, selection/delegation
status, and decision reference to the confirmation. For `static_reference` and
`profile_reuse`, the snapshot includes the exact `built_in_theme=not_required` object
and the selected/delegated motion decision. If any bound field changes, keep the brief
pending, update the customer-readable brief, recompute the canonical digest, and obtain
a new confirmation; reusing the old brief hash or confirmation reference fails closed.
Do not hand-build this digest or parse Markdown to derive it. With both decisions
complete and the brief still pending, run the normal checker flow:

```bash
python3 scripts/check_production_authorization.py \
  --state <current-task-root>/gates/production-state.json \
  --artifact-root <current-task-root> \
  --action design-brief-preview
```

Read `current_design_decisions_sha256` from the successful JSON result. After the
customer confirms the current brief, write that exact value to
`design_brief.design_decisions_sha256` together with the current brief file hash and
confirmation reference, then run the same checker with `--action formal-html`. A
normal `--action status` result exposes the same current digest. The confirmed result
echoes it again; no helper import, ad-hoc serialization, or separate subcommand is
required.

A pending design brief may name its planned artifact path but keeps
`artifact_sha256`, `confirmation_ref`, and `design_decisions_sha256` null. Other
pending confirmation gates keep their digest and confirmation reference null;
`not_required` gates keep every artifact/confirmation field null.

## Allowed-Action Matrix

| Current blocking gate | Allowed next artifact/action | Still forbidden |
|---|---|---|
| Bound material summary unconfirmed | inspect the eligible bound material, render/update the Material Understanding Summary, request its confirmation | VI, design brief, formal HTML, browser QA, delivery |
| Visual route unresolved | ask the one current visual-source decision | VI, design brief, formal HTML, browser QA, delivery |
| Static-reference VI unconfirmed | run the environment/readability gates, render/update the VI standards-board preview, request confirmation/correction of that exact artifact | project theme, design brief, formal HTML, browser QA, delivery |
| Corporate profile selected but binding unvalidated | generate/revalidate the task-local profile-use binding against the live active version and theme | design brief, formal HTML, browser QA, delivery |
| VI confirmed but project theme not compiled | compile the exact confirmed project theme | design brief, formal HTML, browser QA, delivery |
| Built-in theme pending | display the complete applicable catalog (or explicit category subset), recommend 1–2 without hiding entries, and request selection or explicit delegation | design brief, formal HTML, browser QA, delivery |
| Motion density pending | display 少量 / 适中 / 丰富, recommend one, and request selection or explicit delegation | design brief, formal HTML, browser QA, delivery |
| Design brief unconfirmed | render/update the Report Design Brief and request its confirmation | formal HTML, browser QA, delivery |
| Every applicable current gate complete | create/refine formal HTML, run browser QA, deliver formal HTML | none from this authorization contract |

The material summary, VI standards board, profile-use binding, and Report Design Brief are gate artifacts,
not formal report HTML. Do not use “preview” to create or hand over a nearly finished
deck before authorization.

## Machine Gate

Run the bundled checker before the requested action:

```bash
python scripts/check_production_authorization.py \
  --state /absolute/path/to/current-production-authorization.json \
  --artifact-root /absolute/path/to/current-task \
  --action material-summary-preview

python scripts/check_production_authorization.py \
  --state /absolute/path/to/current-production-authorization.json \
  --artifact-root /absolute/path/to/current-task \
  --action reference-vi-preview

python scripts/check_production_authorization.py \
  --state /absolute/path/to/current-production-authorization.json \
  --artifact-root /absolute/path/to/current-task \
  --action built-in-theme-selection

python scripts/check_production_authorization.py \
  --state /absolute/path/to/current-production-authorization.json \
  --artifact-root /absolute/path/to/current-task \
  --action motion-density-selection

python scripts/check_production_authorization.py \
  --state /absolute/path/to/current-production-authorization.json \
  --artifact-root /absolute/path/to/current-task \
  --action formal-html
```

The checker resolves each confirmed or bound file under `--artifact-root`, rejects absolute
paths, traversal, any artifact symlink, missing files, and current-byte hash mismatches. It
also rejects schema drift and impossible ordering, prints JSON, and exits nonzero when
the requested action is not currently allowed. Run `--action formal-html` immediately
before saving the first runnable formal `index.html`; run `--action browser-qa` before
browser QA and `--action deliver-formal-html` before delivery so a post-confirmation
change fails closed at every formal boundary. Preserve the current state and checker
result with task evidence when possible. Never edit the state merely to bypass a gate;
update it only after the corresponding current artifact and confirmation exist.

For profile reuse, set `TAOHTML_HOME` consistently before every checker invocation (or
use the default `~/.taohtml`). Changing active version, archiving the profile, editing
identity metadata, or changing any profile/VI/reference/theme byte invalidates the
binding. Never change the state to built-in merely to bypass a failed profile check.

## Trust Boundary

The task-local path and verified SHA-256 prove that the checked file still has the
bytes recorded at confirmation time. `confirmation_ref` is trace metadata supplied by
the executing Agent; this checker does not access or independently
authenticate the conversation platform. Therefore a missing or malformed reference is
rejected, but the checker does not claim that a non-empty reference proves user intent.
Keep the reference auditable and retain the corresponding conversation evidence under
the platform's own access controls.

The same trust boundary applies to each `decision_ref`: the checker requires a
non-empty reference and a compatible selection status/value, but it cannot inspect the
conversation platform or independently prove that the referenced turn contains the
claimed choice or delegation. Preserve that evidence under the platform's controls.

A profile-use binding does not carry a new customer confirmation reference because
unique reuse proceeds by concise notice and non-objection. Its authority comes only
from exact current enterprise resolution and live file/hash validation. It substitutes
for repeated VI generation, never for the current Report Design Brief confirmation or
any formal-action gate.
