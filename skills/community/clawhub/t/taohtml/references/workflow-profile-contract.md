# Workflow Profile Contract

This contract defines how one installed TaoHtml Skill selects and applies one primary
Workflow Profile. A Profile is a business-production path loaded on demand; it is not
an independently installed Skill, a replacement for intake, or a second production
engine.

## Contents

- [Contract Identity](#contract-identity)
- [Layering Model](#layering-model)
- [Definition Routing](#definition-routing)
- [Routing Contract](#routing-contract)
- [Primary Profile And Capability Overlays](#primary-profile-and-capability-overlays)
- [Horizontal Parameters](#horizontal-parameters)
- [Required Profile Sections](#required-profile-sections)
- [IR Mapping Boundary](#ir-mapping-boundary)
- [Existing Gates And Implementations](#existing-gates-and-implementations)
- [Conflict Resolution](#conflict-resolution)

## Contract Identity

- Contract id: `taohtml.workflow-profile`
- Contract version: `1.1`
- Catalog: `workflow-profiles.md`
- Cardinality: exactly one primary Profile per project after routing is resolved
- Definition status in this engineering node: all nine Profiles are
  detailed/implemented Golden Paths (`formal-submission-writing`,
  `research-analysis-argumentation`, `periodic-operations-reporting`,
  `proposal-planning-decision`, `live-presentation-persuasion`,
  `teaching-training-knowledge-transfer`, `project-lifecycle-reporting`,
  `brand-communication-editorial-publishing`, and
  `rule-response-application-defense`); zero current Profiles remain foundation
  definitions

Each Profile has one stable `profile_id`, one exact customer-facing Chinese name, and
one definition version. The definition version is an internal Profile-contract
identity; it does not by itself change TaoHtml's release version, Report IR schema,
Compiler, Runtime, theme, Handoff schema, or any other implementation version.

## Layering Model

Keep these dimensions independent:

1. Apply the existing `new_build | review_only | continue_existing` task-intent
   overlay from `project-handoff.md` when applicable.
2. Establish one of the existing material entry routes: idea only, Word/PDF, or
   existing PPT/HTML. The Profile layer never adds a fourth entry route.
3. Select one primary Workflow Profile from the user's business objective and the
   semantics of eligible material.
4. Add only bounded capabilities from other Profiles when needed; never run two
   complete Profile workflows in parallel.
5. Resolve horizontal parameters through the existing intake, source, visual,
   Runtime, evidence, and continuation contracts.

The task-intent overlay, material entry, primary Profile, capability overlays, and
horizontal parameters must remain separately recorded. A value in one layer must not
be used as a hidden substitute for another.

## Definition Routing

Use this table for a clear semantic route. Read exactly one `definition_ref`; do not
read `workflow-profiles.md` or any other Profile definition on the clear path.

| profile_id | Exact customer-facing name | definition_ref |
|---|---|---|
| `formal-submission-writing` | 规范报送与正式写作 | `references/workflow-profile-formal-submission-writing.md` |
| `research-analysis-argumentation` | 研究分析与专业论证 | `references/workflow-profile-research-analysis-argumentation.md` |
| `periodic-operations-reporting` | 周期经营与数据汇报 | `references/workflow-profile-periodic-operations-reporting.md` |
| `proposal-planning-decision` | 方案策划与决策提案 | `references/workflow-profile-proposal-planning-decision.md` |
| `live-presentation-persuasion` | 现场演讲与说服表达 | `references/workflow-profile-live-presentation-persuasion.md` |
| `teaching-training-knowledge-transfer` | 教学培训与知识传递 | `references/workflow-profile-teaching-training-knowledge-transfer.md` |
| `project-lifecycle-reporting` | 项目全过程汇报 | `references/workflow-profile-project-lifecycle-reporting.md` |
| `brand-communication-editorial-publishing` | 品牌传播与编辑出版 | `references/workflow-profile-brand-communication-editorial-publishing.md` |
| `rule-response-application-defense` | 规则响应、申报与答辩 | `references/workflow-profile-rule-response-application-defense.md` |

Every `definition_ref` must be unique, non-empty, directly reachable from this
one-level reference table, and contain exactly one Profile definition. After routing,
apply the status declared by that selected definition: a detailed/implemented Golden
Path supplies Profile-specific judgment, sequence, semantic mapping, brief additions,
and QA emphasis while continuing to use every shared gate and implementation. Do not
load a second definition to complete it. A foundation definition remains usable at
its declared foundation scope and must not be presented as a detailed Golden Path.

## Routing Contract

Route by semantic outcome, not by labels alone:

1. Re-read the user's explicit objective, audience outcome, desired decision or
   action, eligible inspected material, confirmed Material Understanding Summary,
   and still-supported handoff state.
2. If one business-production path is clearly dominant, automatically select that
   primary Profile, record the selection basis, read only its `definition_ref` from
   Definition Routing, and continue without reading the catalog, asking a Profile
   question, or loading any other Profile definition.
3. Do not ask again when a prior answer, confirmed report goal, or material semantics
   already establishes the primary Profile. A report-type recommendation is not a
   reason to repeat a known business-goal question.
4. When the primary business objective remains genuinely ambiguous after using the
   eligible semantic evidence, read `workflow-profiles.md`, display all nine exact
   customer-facing Profile names in one round, and ask exactly one routing question:
   which business goal should the finished report primarily accomplish? After the
   answer, read only the selected row's `definition_ref` and apply that selected
   definition. Do not load the other eight definition files.
5. Record that catalog as the latest active option set. A short answer or ordinal can
   select an item only when it directly answers that still-active catalog in the same
   conversation; numbering in documentation is never a global command interface.
6. Ask the user to choose a business objective, never a Profile id, Report IR field,
   Projection, schema property, Compiler mode, Runtime feature, or theme implementation.

Do not route with a keyword blacklist, a hard-coded numeric command, filename-only
matching, directory conventions, or a fixed mapping from report type to Profile.
Terms and document types may contribute semantic evidence, but the deciding question
is the outcome the artifact must accomplish. Do not inspect an unbound source merely
to classify a Profile.

Profile routing uses the existing clarification budget. Automatic routing uses zero
questions; the full-catalog fallback is one routing question. It does not create a
new intake cycle, a nine-part questionnaire, or extra questions beyond the existing
maximum.

## Primary Profile And Capability Overlays

Record the resolved state as:

```text
primary_profile = profile_id | exact name | definition version | selection basis
capability_overlays = bounded capability | source Profile | reason | affected scope
```

The primary Profile owns the overall design-ready interpretation, narrative promise,
and Profile-specific acceptance emphasis. A capability overlay may borrow one bounded
need, such as a data review module, a teaching explanation, or live delivery support.
It must not import a second Profile's complete intake, design-ready gate, narrative
sequence, artifact set, or QA workflow.

If the requested result changes so another business outcome becomes dominant, replace
the primary Profile explicitly. Treat that as a result-changing design decision and
re-evaluate the affected source interpretation and Report Design Brief under the
existing continuation and confirmation rules. Do not silently keep two primary
Profiles.

## Horizontal Parameters

These are cross-cutting parameters, not Profiles. A Profile may provide a low-risk
recommendation only when the value is not already known, confirmed, inherited, or
delegated. The existing source, brief, visual, Runtime, evidence, and Handoff contracts
remain authoritative. A recommendation never becomes a customer decision by default.

| Parameter | Contract boundary |
|---|---|
| `input_entry_route` | Idea only, Word/PDF, or existing PPT/HTML; preserve the existing route handshake and source gate. |
| `use_mode` | Reading or presentation; it remains an existing startup and Runtime/delivery choice, not a scenario. A Profile recommendation applies only after the user explicitly delegates that choice; otherwise preserve or resolve it under `intake-workflow.md`. |
| `visual_binding` | Built-in visual system, confirmed project theme, or validated enterprise Profile binding; never copy theme implementation into a Workflow Profile. |
| `evidence_rigor` | Use the Report IR stable enum directly: `exploratory`, `standard`, or `formal`. No Product-layer aliases are permitted. High-risk and source-protection rules always override the default. |
| `information_density` | Low, medium, or high production guidance after content length and actual material are known. |
| `motion_density` | Use the Report IR stable enum directly: `minimal`, `moderate`, or `rich`, displayed to the customer as 少量 / 适中 / 丰富. A Profile value is recommendation evidence only; the customer must select it or explicitly delegate the choice. No Product-layer aliases are permitted, and the current Runtime contract still constrains implementation. |
| `continuation_state` | New build, review-only, meaning-preserving local continuation, or meaning-changing continuation under the existing Handoff contract. |

Do not ask the user to fill these as a Profile form. Reuse values already established
by conversation, eligible material, the Report Design Brief, or a valid handoff.
`content_length` is not a Profile default: keep the existing concise/standard/detailed
choice and its explicit-delegation requirement. Neither `use_mode` nor content length
may be inferred merely because a Profile supplies other defaults. Likewise, never turn
a Profile's `motion_density` recommendation into a selected value without the
independent design-choice evidence required by `production-authorization.md`.

## Required Profile Sections

Every Profile definition must contain these exact sections:

| Section | Required content |
|---|---|
| 身份与版本 | Stable id, exact name, definition version, and foundation or detailed/implemented status. |
| 适用目标 | The dominant business outcome that makes this the primary Profile. |
| 排除范围 | Nearby outcomes that require another primary Profile or an existing subsystem. |
| 成品 | Customer-usable TaoHtml output within the current delivery boundary. |
| 所需信息 | Business information needed to judge the result; reuse known/source-backed items and never expose a new questionnaire. |
| design-ready 条件 | Profile-specific readiness additions to the existing common gate. |
| 叙事任务 | The jobs the narrative must accomplish, without prescribing fixed pages. |
| 证据规则 | Profile-specific evidence emphasis while retaining common source and hard-boundary rules. |
| 横向参数默认值 | Defaults for the cross-cutting parameters; they never override known or confirmed values. |
| IR 映射边界 | Semantic intent only and the conditions under which the existing explicit IR engineering route may use it. |
| Runtime/主题使用 | Use of existing Runtime and visual routes without copied implementation. |
| QA 验收 | Profile-specific acceptance emphasis in addition to existing objective QA and delivery gates. |
| 能力叠加与冲突处理 | Allowed bounded overlays and the rule for choosing or replacing the primary Profile. |

Keep the catalog lightweight. Store each non-empty Profile definition in its unique
one-level `definition_ref`; do not duplicate complete definitions in the catalog or
create empty placeholders.

## IR Mapping Boundary

Workflow Profiles are upstream semantic guidance, not Report IR routes or Compiler
modes:

- Profile selection itself never activates Report IR or changes Direct HTML from the
  default production path. It adds no IR questionnaire.
- Only an explicit Report IR engineering request or current project Report IR
  authorization may use the IR workflow after the Report Design Brief is confirmed
  and current-file Production Authorization independently permits the action.
- Only an independently authorized Report IR engineering project may derive and write
  the confirmed Profile result into a new `1.1` IR. A separate explicit engineering
  request may inspect, validate, compile, or patch an already supplied `1.0`/`1.1`
  source, but it must not infer or manufacture a missing binding.
- On that separately authorized route, Report IR `1.1` writes the already resolved
  result into the one generic top-level `workflow_profile` binding. The binding owns
  only `primary_profile_id`, Profile `definition_version`, semantic
  `selection_basis`, and bounded `capability_overlays`; it never embeds a Profile
  definition, scenario-specific brief fields, HTML, CSS, JavaScript, theme state, or
  enterprise assets.
- Report IR `1.0` remains legacy unbound. Validator and Compiler must not infer a
  Profile from filenames, titles, archetypes, keywords, themes, enterprise bindings,
  material contents, or any other project state.
- The generic binding records upstream identity and provenance. It does not replace
  the Report Design Brief reference/hash/confirmation, authorize production, choose
  pages or layouts, switch themes or Runtime, increase evidence strength, or ask the
  Compiler to reinterpret `selection_basis`.
- A Profile may still guide the model's authorized upstream derivation of existing
  semantic combinations such as report prototype, evidence rigor, narrative units,
  Projection intent, or optional entities. It must not create scenario-specific IR
  fields, a Profile-triggered Compiler branch, or a Validator bypass.

The Report Design Brief remains the customer-readable source of confirmed business
decisions. IR derivation, when separately authorized, remains downstream and does not
replace Profile routing, brief confirmation, or production authorization.

Record the exact customer-facing name, stable `profile_id`, definition version,
semantic selection basis, and bounded capability overlays in the Report Design Brief.
Profile selection, confirmation of the complete current Report Design Brief, and
Production Authorization are three independent facts. Profile routing adds no
questionnaire or separate confirmation round. Changing the generic binding changes
the IR/build identity and deterministic Build Manifest record, but the Compiler must
not use that change to rewrite content, select pages, alter visual composition, switch
the enterprise or theme binding, or change Runtime behavior.

## Existing Gates And Implementations

Profile selection changes none of these existing behaviors:

- The three material entry routes and conversation-scoped option binding.
- Source binding, PDF preflight, and the Word/PDF/PPT/HTML Material Understanding
  Summary confirmation gate.
- Handoff overlay, source-role/availability distinctions, continuation matrix, and
  four independent structured handoff conclusions.
- Visual source selection, profile reuse, static-reference VI confirmation, and
  project-theme compilation.
- The complete current Report Design Brief and its explicit confirmation.
- Current-file Production Authorization for formal HTML, browser QA, and delivery.
- Direct-HTML default production, existing Runtime and theme implementations,
  objective QA, traceability, and `《待核实内容清单》` delivery.

A Profile may point to these contracts but must not copy their schemas, scripts,
algorithms, theme assets, QA logic, or gate state.

## Conflict Resolution

Apply conflicts in this order:

1. User-confirmed business outcome and responsibility boundary.
2. Hard source, evidence, safety, legal, and action-path boundaries.
3. Existing Handoff, brief-confirmation, and Production Authorization gates.
4. Primary Profile contract.
5. Bounded capability overlays.
6. Profile defaults for horizontal parameters.

When a lower layer conflicts with a higher one, keep the higher rule and record the
deviation or unresolved gap. When an overlay would change the dominant outcome,
required artifact, or acceptance promise, it is no longer an overlay: explicitly
re-route the primary Profile and reapply the affected existing gates.
