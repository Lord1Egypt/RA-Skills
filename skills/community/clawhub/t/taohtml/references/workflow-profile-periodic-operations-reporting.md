# 周期经营与数据汇报

## 身份与版本

- `profile_id`: `periodic-operations-reporting`
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

Use as primary only when the artifact's main job is to explain results, variances,
drivers, risks, opportunities, decisions, and management actions for a weekly,
monthly, quarterly, annual, or other real operating cadence.

Select this Profile from the recurring management question and period-control need.
The presence of KPIs, dates, charts, or an “annual report” label does not by itself
establish periodic operating reporting.

## 排除范围

Use `brand-communication-editorial-publishing` for a brand annual publication whose
main outcome is external narrative or identity. Use `project-lifecycle-reporting` for
a single project's milestone/baseline status. Use `proposal-planning-decision` for a
one-time strategic plan whose main result is approval or option selection.

Do not implement a real-time dashboard, data connector, automatic refresh, online
analysis system, scheduled pipeline, new chart component, fixed KPI questionnaire,
fixed scorecard, card layout, table template, or mandatory management-report outline.
This Profile governs an offline report built from controlled current-task data.

## 成品

A customer-usable offline operating report based on controlled data that helps a
manager see:

- what happened in the current period and what data cutoff/freeze supports that view;
- relative to which honest target, budget, baseline, prior period, prior-year
  comparable, forecast, or other management-relevant basis;
- which drivers are directly supported, which explanations remain inferential, and
  which hypotheses still need validation;
- which risks and opportunities follow from the supported results; and
- which decisions and next actions are required, who owns them, and by when or under
  what condition.

The result uses the existing direct-HTML production chain, Runtime/theme routes,
objective QA, Handoff, and `《待核实内容清单》`. It has no required chapter count,
page count, KPI-card count, dashboard shape, or comparison-table layout.

## 所需信息

Reuse eligible conversation, bound sources, the confirmed Material Understanding
Summary, and still-supported Handoff state before identifying any gap. Maintain the
shared `known | confirmed | inferred | missing` ledger; do not expose the following as
a fixed KPI form or data-extraction checklist.

### 周期、截止与管理问题

Resolve only what is needed to define the operating view:

- reporting period, reporting cutoff, and timezone when it affects inclusion;
- whether data is frozen, final, provisional, still updating, restated, or awaiting
  late inputs;
- audience, management question, decision horizon, and responsibility boundary;
- organizational, product, geography, channel, customer, legal-entity, or other
  scope; and
- target, budget, baseline, comparison periods, forecast, or other reference that
  genuinely answers the management question.

Do not treat the report creation date as the data cutoff or silently include post-
cutoff changes.

### 指标与可比性状态

For every important metric, record:

- exact definition, unit/currency, numerator and denominator where applicable;
- included/excluded population, organization, geography, channel, and time window;
- source identity/version, cutoff, aggregation level and method, and revision status;
- target/budget/baseline and comparison-period definitions; and
- how totals, components, rates, shares, growth, variance, and repeated references
  reconcile.

Keep these states distinct in working records, the brief, pages, charts, and delivery:

- `actual`;
- `target / budget`;
- `forecast`;
- `projection / simulation`;
- `restated / revised data`; and
- `unknown | withheld | pending`.

If definition, organization scope, currency, time window, denominator, aggregation,
or source changes, periods are not directly comparable. Explain the change and
recalculate on a common basis, provide an honest bridge, or label the comparison
`not comparable`. Never allow incompatible data to be compared silently.

### 数据质量与驱动状态

Identify material data risks:

- incomplete data, late-arriving records, missing segments, duplicate rows, revised
  or restated values, abnormal values, source conflicts, and post-cutoff change risk;
- prior-period figures copied from older reports whose definitions or revision state
  may no longer match; and
- missing detail that prevents a total, variance, or driver claim from being checked.

Classify every important driver as one of:

- `数据直接支持的 driver`;
- `基于材料的解释`;
- `待验证 hypothesis`; or
- `外部因素` with its actual evidence and scope.

Correlation, timing, or a management narrative does not automatically establish a
causal driver. State the evidence strength and what would validate the explanation.

### 最大缺口规则

After each pass, ask at most the one largest still-missing data item whose answer
could change the operating conclusion, risk assessment, management decision, or
action. Reuse the shared 0-6 question budget, repetition rule, information-gain stop,
and hard boundaries; do not add a KPI questionnaire or fixed retrieval list.

When critical data is missing, stale, or incomparable, retain supported metrics and
mark affected results `withheld | pending`. If the gap could overturn the overall
conclusion, block a formal cycle review or continue only after the user explicitly
accepts a `preliminary / data-gap review`. Do not invent performance, targets,
budgets, causes, risks, owners, actions, completion status, or management decisions.

## design-ready 条件

The shared design-ready gate must pass, plus these operating decisions must be
sufficiently clear for the honest delivery class:

- reporting period, cutoff, applicable timezone, data-freeze/update state, audience,
  management question, and organization/business scope;
- every important metric's definition, unit/currency, numerator/denominator, range,
  aggregation, source/version, cutoff, and revision status;
- target, budget, baseline, and comparison periods selected for the real management
  question without cherry-picking;
- comparison compatibility, with definition/scope/currency/window/denominator/source
  changes recalculated, bridged, or labeled not comparable;
- data completeness, late/missing segments, anomalies, duplicates, restatements,
  conflicts, post-cutoff risk, and affected conclusions;
- key variances and driver explanations at their actual evidence strength; and
- risks/opportunities, required decisions, actions, owners, timing/conditions, and
  current action status without inventing responsibility or completion.

A formal periodic result is design-ready only when critical data is current enough,
comparable enough, and complete enough for the claimed management conclusion.
Supported metrics may remain visible while affected conclusions are withheld or
pending. A user-accepted `preliminary / data-gap review` may become design-ready when
its checked scope and gaps are clear, but the preliminary boundary must remain in the
brief, every summary/conclusion page, delivery wording, and Handoff. It must not be
packaged as a complete formal period review.

### 设计简报增量

Write these customer-readable fields inside the one existing Report Design Brief's
adaptive `场景特有决策` section. Reuse the current ledger; do not create a second
brief or KPI form, and do not add a Profile-specific confirmation round.

- `经营周期与 cutoff`: reporting period, cutoff, applicable timezone, freeze/
  update state, and post-cutoff handling;
- `管理问题`: audience, decision horizon, scope, and what management must
  understand or decide;
- `指标与口径`: important metric definitions, units/currencies,
  numerators/denominators, ranges, aggregation, sources, and revisions;
- `比较基准`: target, budget, baseline, prior-period/prior-year/forecast or
  other comparison, plus compatibility and bridge status;
- `数据完整性与修订`: completeness, late/missing segments, anomalies,
  duplicates, restated/revised values, source conflicts, and cutoff risk;
- `关键差异/驱动`: material variances, directly supported drivers,
  source-based explanations, hypotheses, external factors, and causal limits;
- `风险机会`: risks and opportunities linked to the relevant metrics and drivers;
- `决策/行动/owner`: required decisions, actions, accountable owners, time or
  condition, and `计划 | 进行中 | 完成 | 已验证效果` status;
- `关键限制`: withheld/pending metrics, non-comparable periods, missing proof,
  and what could overturn the conclusion; and
- `交付边界`: formal or preliminary/data-gap class, supported conclusion
  scope, unresolved items, and what the report does not establish.

Record reversible inferences and their bases in the existing `待确认项`. Display and
confirm the complete current brief once. Profile selection, complete-brief
confirmation, and current-file Production Authorization remain three independent
facts.

## 叙事任务

### Golden Path

1. **Enter through shared state.** Establish or inherit the material route, task
   intent, use mode, content length, source bindings, and exactly one primary Profile.
   Do not route here from KPI/date/report labels alone or reopen known horizontal
   values.
2. **Bind the operating frame.** Establish the period, cutoff/timezone, freeze/update
   state, management question, scope, and responsibility boundary. Ask only the
   current largest result-changing data gap when one remains.
3. **Govern metrics before comparison.** Bind each important metric to its source,
   version, cutoff, definition, unit/currency, numerator/denominator, scope,
   aggregation, revision state, and comparison basis. Recalculate, bridge, or label
   incompatible periods rather than comparing them silently.
4. **Reconcile the result and variance.** Verify totals/components, growth rates,
   percentage-point changes, shares, year-over-year/period-over-period comparisons,
   budget variances, and repeated values. Keep actual, target/budget, forecast,
   projection/simulation, revised, and unknown states distinct.
5. **Explain drivers at honest strength.** Separate data-supported drivers,
   source-based explanations, hypotheses, and external factors. Preserve contrary
   movement and unknowns; correlation does not become causation through a chart or
   management narrative.
6. **Connect insight to management action.** Link risks, opportunities, decisions,
   and actions to the relevant metric/driver. State owner, time or condition, current
   status, and next check. Keep `计划`, `进行中`, `完成`, and `已验证效果`
   separate.
7. **Choose the honest delivery branch.** Use the formal branch only when critical
   data is current, compatible, and sufficient. Otherwise withhold affected results,
   block as necessary, or use only the explicitly accepted preliminary/data-gap
   branch and preserve that boundary through pages, delivery, and Handoff.
8. **Build the management sequence from the question.** Usually complete period
   overview → key target/baseline variances → material drivers and counter-movements
   → risks/opportunities → required decisions → owned next actions. Use only the
   jobs the actual report needs; do not turn this into a fixed chapter or page
   template.
9. **Use the one shared brief and authorization chain.** Add only the fields above to
   the current Report Design Brief, obtain its ordinary complete-brief confirmation,
   then pass current-file Production Authorization. Do not add another confirmation
   or treat Profile selection as production authority.
10. **Produce through the existing chain.** After authorization, follow
    `process-playbook.md`, save the first runnable direct-HTML artifact, apply the
    validated visual route and current Runtime, then run specialized plus shared QA
    and delivery gates.

### 页面任务与经营表达

Give each page one real management job, such as showing a result, explaining a
variance, testing a driver, exposing a risk or opportunity, making a decision
request, assigning an action, or stating a data limitation. Use the visual form that
makes the real relationship checkable. These are semantic tasks, not mandatory KPI
cards, dashboards, tables, charts, or page layouts.

## 证据规则

- Bind every important metric to source/version, cutoff, unit/currency, numerator and
  denominator, included scope, aggregation method, revision status, and comparison
  basis. File existence or an old chart does not establish current metric validity.
- Keep mathematical relationships reproducible. Do not mix total and component,
  growth rate and percentage-point change, share and rate, year-over-year and period-
  over-period, or target/baseline/budget variance.
- Label actual, target/budget, forecast, projection/simulation, restated/revised data,
  and unknown/withheld/pending consistently in chart, title, body, source, and
  summary language.
- Classify driver evidence honestly as directly supported, source-based explanation,
  hypothesis, or external factor. Correlation and timing do not automatically prove
  causation.
- Choose comparisons to answer the real management question, not to maximize a
  favorable narrative. Show target, prior period, prior-year comparable, forecast, or
  another basis when each is materially useful, without forcing a fixed combination.
- Link each material risk, opportunity, decision, and action to the relevant
  metric/driver. State owner and time/condition only from eligible material or
  explicit confirmation. Never turn a plan or ongoing action into completed work or
  verified effect.
- When reusing a prior period, verify definitions and revision consistency. Do not
  leave an old chart beside a newly restated figure or silently mix old and new
  metric bases.
- Never invent performance, targets, budgets, forecasts, causes, risks, opportunities,
  owners, actions, completion status, management decisions, data sources, or
  calculations. Apply shared output-first rules only outside these hard boundaries.

## 横向参数默认值

- `input_entry_route`: inherit the established material route
- `use_mode`: `reading` recommendation only after explicit delegation; otherwise inherit or resolve the existing startup choice
- `visual_binding`: inherit the validated visual route
- `evidence_rigor`: `formal`
- `information_density`: `high`
- `motion_density`: `minimal` recommendation only; require customer selection or explicit delegation
- `continuation_state`: inherit the Handoff decision

These defaults never override a known, confirmed, inherited, or explicitly delegated
horizontal value. `content_length` remains the shared independent choice. A
preliminary/data-gap branch may lower the actually supportable evidence posture
without silently replacing any other horizontal value.

## IR 映射边界

Direct HTML remains the default. Only when the IR engineering route is independently
authorized may this Profile guide existing dataset, data-visualization, `claim`,
`evidence`, `source`, comparison, process, traceability, page-task, and Projection
semantics.

Do not add KPI, numerator, denominator, cutoff, revision, driver, owner, action-status,
or management-decision fields to the Report IR Schema. Do not create a fixed JSON
operating model, dashboard engine, data connector, automatic refresh path, online
analysis system, metric-scoring algorithm, Profile-triggered IR path, Compiler branch,
or incremental compilation route. The customer-readable operating state belongs in
the confirmed Report Design Brief and project-local working record; any authorized
IR remains downstream.

## Runtime/主题使用

Use only the established reading or presentation mode, validated built-in/project/
enterprise visual route, current data/chart treatments, and current Runtime. Existing
page semantics and `fragment-v1` may support spoken explanation when the confirmed
mode requires it.

The Profile does not add a dashboard, live chart, data refresh, connector, drill-down,
dual-screen presenter view, cross-page morphing, complex state, new visualization
component, or new Runtime control. Theme and animation cannot change metric meaning,
data freshness, comparability, or driver strength.

## QA 验收

Run all existing objective QA, traceability, asset/browser QA, current-file
authorization rechecks, Runtime/editor checks where applicable, Handoff validation,
and delivery gates. In addition, verify:

- `metric math`: numerator/denominator, unit/currency, aggregation, time interval,
  cutoff, and applicable timezone are correct and reproducible;
- actual, target/budget, forecast, projection/simulation, revised, and unknown states
  agree across chart, title, body, source, summary, and conclusion;
- year-over-year/period-over-period, percentage/percentage point, total/component,
  share/rate, target/baseline, and budget-variance calculations are not mixed and
  repeated values remain identical;
- data source/version, cutoff, revision/restatement, and the values used in charts,
  tables, body text, and summaries remain source-consistent;
- comparisons preserve definition, scope, currency, time window, denominator,
  aggregation, and source compatibility, or show an accurate bridge/not-comparable
  boundary;
- driver language matches evidence strength; risks/opportunities connect to the
  supported metric/driver; decisions and actions name confirmed owners and time or
  conditions with honest status;
- incomplete, stale, late, revised, conflicting, or incomparable data is never used
  silently for a formal conclusion; affected metrics remain withheld/pending where
  required; and
- preliminary/data-gap results remain explicitly non-final throughout summaries,
  conclusion pages, delivery wording, and Handoff rather than becoming a complete
  formal period review.

Any failure remains a Profile-specific QA failure in addition to the shared gate; it
does not replace or collapse existing QA and delivery conclusions.

## 能力叠加与冲突处理

Research explanation, decision framing, project detail, formal writing, or live
delivery may be bounded overlays with a stated source Profile, reason, and affected
scope. They may not import another Profile's complete intake, design-ready gate,
narrative sequence, artifact set, or QA workflow.

Keep this Profile primary while recurring period performance and management action
remain the dominant product. Switch to `brand-communication-editorial-publishing`
for an external brand annual narrative, `project-lifecycle-reporting` for a single
project baseline/milestone report, or `proposal-planning-decision` for a one-time
strategic option decision. Rebuild only affected decisions, reuse the existing
complete-brief confirmation, and never run two Golden Paths in full.
