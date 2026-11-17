# 项目全过程汇报

## 身份与版本

- `profile_id`: `project-lifecycle-reporting`
- Definition version: `2.0`
- Status: detailed/implemented Golden Path
- Shared workflow dependencies: `intake-workflow.md`, `material-understanding.md`,
  `design-brief-template.md`, `production-authorization.md`, `process-playbook.md`,
  `runtime-contract.md`, and `project-handoff.md`

### 目录

- [适用目标](#适用目标)
- [排除范围](#排除范围)
- [成品](#成品)
- [所需信息](#所需信息)
- [design-ready 条件](#design-ready-条件)
- [叙事任务](#叙事任务)
- [证据规则](#证据规则)
- [横向参数默认值](#横向参数默认值)
- [IR 映射边界](#ir-映射边界)
- [Runtime/主题使用](#runtime主题使用)
- [QA 验收](#qa-验收)
- [能力叠加与冲突处理](#能力叠加与冲突处理)

## 适用目标

Use as primary only when stakeholders must govern one specific project through its
objective, scope, baseline, phase, progress, changes, risks, decisions, results, or
closeout state, and the artifact must support an honest project conclusion at a
declared reporting cutoff.

Select this Profile from the concrete project identity and governance outcome. A
project name, timeline, milestone list, or request for a progress report does not by
itself establish this Profile.

## 排除范围

Use `periodic-operations-reporting` when organization-level results and management
actions repeat on an operating cadence rather than following one project baseline.
Use `proposal-planning-decision` when the dominant product is selection or approval
of a plan that has not yet become the governed project baseline. Use
`rule-response-application-defense` when external eligibility, mandatory response,
scoring, or submission rules decide success.

Do not create a fixed project-management method, phase count, weekly-report template,
Gantt chart, status card system, page count, chapter outline, project database, live
status integration, portfolio tool, issue tracker, or acceptance workflow.

## 成品

A customer-usable offline HTML project report adapted to the project's actual phase,
with:

- project identity, objective, sponsor/audience, scope baseline and version, current
  phase, and reporting cutoff;
- milestones, deliverables, dependencies, issues, risks, changes, decisions, and
  actions at their real evidence-backed status;
- baseline, current state, and forecast kept distinct;
- delivered, accepted, and closed states kept distinct from file existence,
  production completion, and Handoff; and
- the existing current-file authorization, objective QA, Handoff, delivery, and
  `《待核实内容清单》` boundaries.

The result has no required project method, phase count, chapter count, page count,
milestone table, Gantt shape, dashboard, or card layout. Its narrative and delivery
class must match the actual project stage: a progress or closeout-readiness draft is
not an accepted or closed project.

## 所需信息

Reuse eligible conversation, bound sources, the confirmed Material Understanding
Summary, and still-supported Handoff state before identifying a gap. Maintain the
shared `known | confirmed | inferred | missing` ledger; do not expose the following
as a fixed project form, status sheet, or retrieval checklist.

### 项目身份、基线与 cutoff

Resolve only what is needed to frame the current governance view:

- project identity, objective, sponsor, audience, governance purpose, and decision
  horizon;
- scope baseline, baseline version/date, included and excluded work, approved success
  or acceptance criteria, and responsibility boundary;
- current phase and the evidence that establishes it;
- reporting cutoff and applicable timezone when it changes which records are in
  scope; and
- completion, acceptance, benefits-realization, closeout, and unresolved-obligation
  conditions.

Do not treat the report creation date as the project cutoff. Do not silently combine
records from different baseline versions or post-cutoff events.

### 计划、状态与验收状态

Reuse real plans, milestones, deliverables, work records, dependencies, issues,
risks, changes, decisions, owners, and evidence. Keep these project states distinct
in working records, the brief, pages, summaries, and delivery:

- `planned`;
- `in progress`;
- `blocked`;
- `delivered`; and
- `accepted`;
- `closed`.

An existing file may show that work was produced. A delivery record may support
`delivered`. Only eligible acceptance evidence or explicit authorized confirmation
supports `accepted`; only satisfied closeout conditions support `closed`. Project
Handoff is a continuation and transition index, not external project acceptance
evidence.

Bind every material milestone date, completion percentage, status, owner, delivery,
acceptance, and closure statement to an eligible record or explicit confirmation.
When exact percentage is not supported, use the honest qualitative state rather than
inventing precision.

### 基线、变化与治理分类

Keep `baseline`, `current`, and `forecast` distinct. For every material change, keep
these levels separate:

- `proposed change`;
- `approved change`; and
- `implemented change`.

Record the actual decision authority, date, affected baseline version, and impact on
scope, time, cost, quality, risk, or benefit where supported. A proposal is not an
approval; an approval is not proof that implementation occurred; implementation does
not silently rewrite the historical baseline.

Also keep `issue`, `risk`, `dependency`, `decision`, and `action` distinct. State how
they relate, their current status, and only sourced or confirmed owners and dates. A
current issue is not merely a future risk, a dependency is not automatically a
blocker, a decision is not an action, and an action is not completed merely because
it was assigned.

### 最大缺口规则

After each pass, ask at most the one largest still-missing item whose answer could
change project status, governance conclusion, acceptance/closure claim, required
decision, or responsibility boundary. Reuse the shared 0-6 question budget,
repetition rule, information-gain stop, and hard boundaries; do not add a project
questionnaire, fixed status table, or independent confirmation round.

When evidence is incomplete, retain supported states and mark affected items
`pending | unknown`. If the user requests a formal completion or closeout conclusion
without adequate acceptance evidence, block that conclusion or continue only after
the user explicitly changes the result to a `progress / closeout-readiness draft`.
That draft must remain unaccepted and unclosed in the brief, every summary or
conclusion page, delivery wording, and Handoff.

## design-ready 条件

The shared design-ready gate must pass, plus these project decisions must be
sufficiently clear for the honest delivery class:

- project identity, objective, sponsor/audience, governance purpose, and responsibility
  boundary;
- scope baseline, version/date, included/excluded work, current phase, reporting
  cutoff, and applicable timezone;
- success, delivery, acceptance, benefit, closeout, and unresolved-obligation
  conditions;
- material milestones/deliverables, dates, statuses, owners, completion evidence,
  dependencies, and acceptance state;
- baseline/current/forecast distinctions and the source/version/cutoff boundary for
  each material status;
- proposed/approved/implemented changes, authority, date, affected baseline, and
  impacts on scope, time, cost, quality, risk, or benefit;
- issues, risks, dependencies, decisions, and actions classified honestly and linked
  to sourced owners, dates, states, and evidence; and
- critical gaps, conflicts, pending/unknown states, required decisions, next actions,
  and the formal or draft delivery boundary.

A formal closeout result is design-ready only when delivery, acceptance, remaining
obligations, and closure conditions are evidenced at the claimed strength. A
`progress / closeout-readiness draft` may become design-ready when its checked scope
and gaps are clear, but it must not be packaged as accepted or closed.

### 设计简报增量

Write these customer-readable fields inside the one existing Report Design Brief's
adaptive `场景特有决策` section. Reuse the current ledger; do not create a second
brief, project ledger, independent confirmation, or authorization. Do not add a
Profile-specific confirmation round.

- `项目目标、sponsor/受众与治理目的`: project identity, objective, sponsor,
  audience, responsibility boundary, and intended governance result;
- `baseline/范围版本`: baseline version/date, included and excluded scope, success
  basis, and historical/current boundary;
- `当前阶段与 reporting cutoff`: phase, cutoff, applicable timezone, evidence
  coverage, and post-cutoff handling;
- `里程碑/交付物及状态证据`: milestone/deliverable, date, owner, honest state,
  completion basis, delivery, and acceptance evidence;
- `变化/偏差与影响`: baseline/current/forecast variance plus proposed/approved/
  implemented change, authority, date, and impact;
- `issue/risk/dependency`: category, relationship, probability or actuality boundary,
  owner, date/condition, status, and evidence;
- `所需决策、行动与 owner`: decision authority, action, owner, due date/condition,
  current state, and next check;
- `验收/收尾条件、未结义务`: delivery, acceptance, benefits, closeout conditions,
  unresolved obligations, and the evidence required to move each state;
- `关键缺口与状态结论`: pending/unknown items, conflicts, unsupported percentages,
  missing acceptance evidence, and the currently supportable conclusion; and
- `交付边界`: formal progress/closeout result or `progress / closeout-readiness
  draft`, unresolved items, and what the artifact does not establish.

Record reversible inferences and their bases in the existing `待确认项`. Display and
confirm the complete current brief once. Profile selection, complete-brief
confirmation, and current-file Production Authorization remain three independent
facts.

## 叙事任务

### Golden Path

1. **Enter through shared state.** Establish or inherit the material route, task
   intent, use mode, content length, source bindings, and exactly one primary Profile.
   Do not route here from a project name, timeline, or progress-report label alone,
   and do not reopen known horizontal values.
2. **Bind the project frame.** Establish project identity, objective, sponsor/audience,
   governance purpose, scope baseline/version, current phase, reporting cutoff,
   responsibility, and acceptance/closeout conditions. Ask only the current largest
   result-changing gap when one remains.
3. **Reconstruct the evidence-backed state.** Connect plans, milestones,
   deliverables, dates, owners, work records, dependencies, issues, risks, changes,
   decisions, actions, delivery, and acceptance evidence. Keep file existence,
   delivered, accepted, and closed distinct.
4. **Separate time and change layers.** Show baseline, current, and forecast without
   silent version mixing. Classify each material change as proposed, approved, or
   implemented and trace its authority, date, affected baseline, and impact.
5. **Reconcile governance categories.** Separate issues, risks, dependencies,
   decisions, and actions; connect them where the relationship matters. Use owners,
   dates, percentages, and statuses only at their supported strength.
6. **Choose the honest project branch.** Use a formal progress or closeout conclusion
   only when its state and acceptance evidence support it. Otherwise preserve
   pending/unknown states, block as necessary, or use only the explicitly accepted
   `progress / closeout-readiness draft` branch through pages, delivery, and Handoff.
7. **Build the sequence from the actual phase.** Usually perform the jobs of objective
   and baseline → current phase/cutoff → completed and remaining work → changes or
   variance and causes → issues/risks/dependencies → required decisions → owners and
   next steps. At closeout, emphasize delivery, acceptance, unresolved obligations,
   and closure conditions. Do not turn these jobs into fixed chapters.
8. **Keep outcome and benefit claims honest.** A deliverable's existence does not
   establish acceptance, benefit, or impact. Preserve future benefits as forecast or
   pending validation until real outcome evidence exists.
9. **Use the one shared brief and authorization chain.** Add only the fields above to
   the current Report Design Brief, obtain its ordinary complete-brief confirmation,
   then pass current-file Production Authorization. Do not add another confirmation
   or treat Profile selection as production authority.
10. **Produce through the existing chain.** After authorization, follow
    `process-playbook.md`, save the first runnable direct-HTML artifact, apply the
    validated visual route and current Runtime, then run specialized plus shared QA
    and delivery gates.

### 页面任务与项目治理表达

Give each page one real governance job, such as establishing a baseline, locating a
phase, showing a milestone or deliverable state, explaining a change or variance,
exposing an issue/risk/dependency, requesting a decision, assigning an action, showing
an outcome, or bounding acceptance and closeout. These are semantic tasks, not fixed
Gantt charts, tables, dashboards, cards, chapters, or page layouts.

Repeat a milestone or status only when it serves another governance job, and preserve
the same date, owner, state, percentage, source, and cutoff each time. Summaries must
not upgrade a detailed page's pending or unknown state.

## 证据规则

- Bind every material baseline, phase, milestone, deliverable, date, completion
  percentage, state, owner, change, decision, delivery, acceptance, result, and closure
  statement to an eligible record or explicit authorized confirmation.
- File existence, production completion, successful TaoHtml delivery, or Project
  Handoff does not equal stakeholder acceptance. Acceptance and closure require their
  own evidence and satisfied conditions.
- Keep planned, in progress, blocked, delivered, accepted, and closed distinct. Keep
  baseline, current, and forecast distinct. Keep proposed, approved, and implemented
  change distinct in detailed pages and summaries.
- Classify issue, risk, dependency, decision, and action honestly. Preserve their
  relationship without collapsing one into another, and never invent an owner, date,
  probability, impact, decision, completion state, or acceptance.
- Do not invent milestones, dates, percentages, status, owners, approvals, results,
  benefits, acceptance, or closure. Use `pending | unknown` or qualitative state when
  precise support is absent.
- A delivered output does not prove an outcome or benefit. Keep future benefits as
  forecast and achieved benefits as pending verification until eligible evidence
  establishes them.
- Apply the shared source-role/availability, high-risk verification, output-first,
  and `《待核实内容清单》` rules without allowing creative supplements to cross the
  project-status, acceptance, or closure boundary.

## 横向参数默认值

- `input_entry_route`: inherit the established material route
- `use_mode`: `reading` recommendation only after explicit delegation; otherwise inherit or resolve the existing startup choice
- `visual_binding`: inherit the validated visual route
- `evidence_rigor`: `formal`
- `information_density`: `high`
- `motion_density`: `minimal` recommendation only; require customer selection or explicit delegation
- `continuation_state`: inherit the Handoff decision

These defaults never override a known, confirmed, inherited, or explicitly delegated
horizontal value. `content_length` remains the shared independent choice. A closeout
label never silently changes evidence rigor or the confirmed use mode.

## IR 映射边界

Direct HTML remains the default. Only when the IR engineering route is independently
authorized may this Profile guide existing timeline, process, comparison, claim,
evidence, source, appendix, page-task, narrative-unit, and Projection semantics.

Do not add project, baseline, phase, milestone, percentage, owner, change-status,
issue, risk, dependency, decision, action, acceptance, or closure fields to the Report
IR Schema. Do not create a fixed JSON project model, project database, status engine,
Gantt generator, live integration, Profile-triggered IR path, Compiler branch, or
Validator bypass. The customer-readable project state belongs in the confirmed Report
Design Brief and project-local working record; any authorized IR remains downstream.

## Runtime/主题使用

Use only the established reading or single-screen presentation mode, validated
built-in/project/enterprise visual route, current page semantics, and current Runtime.
Existing static composition and `fragment-v1` may explain milestones, changes, or a
decision sequence when the confirmed mode requires it.

The Profile does not add a project-management theme, live timeline, Gantt engine,
project database, automatic refresh, persistent issue state, dual-screen presenter
view, cross-page morphing, complex state, or new Runtime control. Theme and animation
cannot upgrade delivery to acceptance or a forecast to an achieved result.

## QA 验收

Run all existing objective QA, traceability, asset/browser QA, current-file
authorization rechecks, Runtime/editor checks where applicable, Handoff validation,
and delivery gates. In addition, verify:

- `baseline/current/forecast`: scope version, phase, reporting cutoff, applicable
  timezone, and post-cutoff handling remain explicit and consistent;
- milestone/deliverable identity, planned and actual dates, state, owner, completion
  percentage, source, delivery, acceptance, and every repeated reference agree;
- every material change is correctly classified as proposed, approved, or implemented,
  with authority, date, affected baseline, and scope/time/cost/quality/risk/benefit
  impact at its real evidence strength;
- issues, risks, dependencies, decisions, and actions are classified distinctly,
  linked correctly, and carry only supported owners, dates/conditions, status, and
  responsibility;
- delivered, accepted, and closed states resolve to the required evidence and
  conditions, and neither file existence nor Project Handoff is used as acceptance;
- project results and benefits do not exceed the evidence, while future benefit stays
  forecast or pending validation;
- a `progress / closeout-readiness draft` remains unaccepted and unclosed throughout
  summary pages, detailed pages, delivery wording, and Handoff; and
- the exact current artifact still passes shared technical, browser, asset,
  authorization, Handoff, and delivery checks without claiming a live project system.

Any failure remains a Profile-specific QA failure in addition to the shared gate; it
does not replace or collapse existing QA and delivery conclusions.

## 能力叠加与冲突处理

Periodic metrics, research explanation, decision framing, formal writing, or live
delivery may be bounded overlays with a stated source Profile, reason, and affected
scope. They may not import another Profile's complete intake, design-ready gate,
narrative sequence, artifact set, or QA workflow.

Keep this Profile primary while governance of one concrete project baseline and phase
remains the dominant product. Switch to `periodic-operations-reporting` for recurring
organization-level operating control, `proposal-planning-decision` for an unapproved
plan choice, or `rule-response-application-defense` when external rules decide
success. Rebuild only affected decisions, reuse the existing complete-brief
confirmation, and never run two Golden Paths in full.
