# 方案策划与决策提案

## 身份与版本

- `profile_id`: `proposal-planning-decision`
- Definition version: `2.0`
- Status: detailed/implemented Golden Path
- Shared workflow dependencies: `intake-workflow.md`, `design-brief-template.md`,
  `production-authorization.md`, `process-playbook.md`, `runtime-contract.md`, and
  `project-handoff.md`

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

Use as primary when a defined decision maker must choose, approve, fund, prioritize,
or authorize a plan based on real options, criteria, evidence, trade-offs,
recommendation, and implementation responsibility.

The decision can be strategic, operational, investment-related, organizational, or
project-specific. The Profile is selected by that dominant outcome, not by the file
type, a proposal label, a comparison layout, or `reading` mode.

## 排除范围

Do not use as primary when live stage performance itself is the main product, when the
artifact only reports recurring results, or when success is governed by an external
application or scoring rule rather than the decision case.

Do not use this Profile to invent a decision matrix, scoring engine, financial model,
workflow questionnaire, fixed page template, or a second approval artifact. Research,
data review, or live delivery may be bounded capabilities; they do not become a
second complete Profile.

## 成品

A decision-ready offline HTML proposal that lets the responsible person understand:

- the decision and why it is due now;
- the real option set and the provenance or disposition of each option;
- the criteria, evidence, assumptions, and material trade-offs;
- the recommendation, its premises, failure conditions, and residual risks; and
- the implementation owner, resource/time boundary, and next decision.

The result uses the existing direct-HTML production chain, QA, delivery evidence, and
`《待核实内容清单》`. It has no required chapter count, page count, card count, or
comparison-matrix shape.

## 所需信息

Reuse eligible conversation, source, confirmed Material Understanding Summary, and
still-supported handoff state before identifying a gap. Maintain the shared
`known | confirmed | inferred | missing` ledger; do not expose the following as a
fixed form.

### 决策定义状态

Resolve only what is needed to make the current decision case honest and usable:

- who makes the decision and who owns the resulting responsibility;
- what must be decided, and what is outside the decision boundary;
- why a decision is required now;
- what no decision or maintaining the status quo means;
- material constraints, non-negotiables, dependencies, and responsibility limits.

### 选项与比较状态

Track each option separately with a customer-readable provenance/disposition:

- `客户提供的选项` for an option supplied by the customer or eligible source;
- `Agent 提议的候选方案` for a generated candidate that remains a proposal rather
  than an established fact; and
- `已淘汰方案` with the known reason and evidence boundary, without silently erasing
  it from the decision record.

Include maintaining the status quo only when it is a real choice or necessary
baseline. Record the evaluation criteria and any known weight, cost, benefit, risk,
reversibility, or implementation condition separately. Do not invent weights merely
to make the options appear comparable.

### 最大缺口规则

After each pass, ask at most the one largest still-missing item whose answer could
change the option set, recommendation, scope promise, or responsibility boundary.
Reuse the shared intake question budget, repetition rule, information-gain stop, and
hard boundaries. Route ordinary missing examples or expression to creative
supplements instead of extending intake.

When viable options do not yet exist, record that option generation or source
recovery is required. When options exist but lack a common honest basis, use a
bounded qualitative comparison or state that the relevant dimension is unknown. Do
not fabricate a complete matrix to create an appearance of certainty.

## design-ready 条件

The shared design-ready gate must pass, plus all result-changing parts of the decision
case must be sufficiently clear:

- decision, decision maker, urgency, boundary, and consequence of no decision;
- a truthful viable option set, or an explicit reason the artifact is proposing or
  narrowing candidates rather than comparing established options;
- stable evaluation criteria whose meaning is not being changed to favor a result;
- visible evidence, assumption, projection, uncertainty, and contradiction boundary;
- recommendation responsibility, implementation boundary, failure conditions, and
  residual risk; and
- the existing verified real action path only when the confirmed objective requires
  an external action.

### 设计简报增量

Write the following customer-readable fields inside the one existing Report Design
Brief's adaptive `场景特有决策` section. Reuse the current ledger; do not create a
second brief, Profile questionnaire, or Profile-specific confirmation round.

- `决策问题`: the exact choice to be made and why it is due now;
- `决策人及责任边界`: decision maker, accountable owner, and limits;
- `选项集合及来源状态`: each option plus `客户提供的选项 | Agent 提议的候选方案 | 已淘汰方案`;
- `评价标准`: criterion meaning, known weight or explicitly unweighted status, and
  evidence boundary;
- `关键取舍`: material cost, benefit, risk, reversibility, and implementation
  condition distinctions;
- `推荐依据`: trace from criteria and evidence to the recommendation;
- `实施责任`: owners, steps, resources, time boundary, and next decision; and
- `风险与失效条件`: recommendation premises, failure conditions, unresolved
  contradictions, and residual risks.

Record every reversible inference and its basis in the existing `待确认项`. Display
and confirm the complete current brief once. Brief confirmation remains distinct from
current-file Production Authorization.

## 叙事任务

### Golden Path

1. **Enter through shared state.** Establish or inherit the material route, task
   intent, use mode, content length, source bindings, and one primary Profile under
   the shared contracts. Do not reopen known decisions.
2. **Define the decision.** Make the decision maker, decision, urgency, status-quo
   consequence, boundary, constraints, and responsibility owner explicit. Ask only
   the current largest result-changing gap when one remains.
3. **Establish the honest option set.** Separate customer-provided, Agent-proposed,
   and eliminated options. Include status quo only when meaningful. If options are
   absent or not honestly comparable, say so and choose a narrative role such as
   candidate generation, feasibility screening, or bounded qualitative comparison;
   never manufacture a full matrix.
4. **Compare without moving the goalposts.** Apply criteria consistently across
   applicable options. Keep facts, assumptions, and projections distinct; expose
   cost, benefit, risk, reversibility, implementation conditions, contrary evidence,
   and unknowns. Never change weights after seeing the result, hide a disconfirming
   option, or back-fit criteria to the preferred recommendation.
5. **Recommend and land.** Trace the recommendation to the visible criteria,
   evidence, and trade-offs. Show its prerequisites, failure conditions, residual
   risks, implementation steps, owners, resource/time boundary, and the next decision.
   Apply the shared action-path rule only if the desired result requires an external
   action.
6. **Use the one shared brief and authorization chain.** Add only the fields above to
   the current Report Design Brief, obtain its ordinary complete-brief confirmation,
   then pass current-file Production Authorization. Do not introduce another
   confirmation or treat brief confirmation as formal-production permission.
7. **Produce through the existing chain.** After authorization, follow
   `process-playbook.md`, save the first runnable direct-HTML artifact, apply the
   validated visual route and existing Runtime, and run the specialized plus shared
   QA and delivery gates.

### 页面任务与视觉重点

Derive pages from the actual decision narrative. Useful semantic page roles include
decision framing, option provenance, bounded comparison, decisive evidence,
trade-off, recommendation, risk boundary, and implementation closure. Use composition
and emphasis to make comparison relationships, contrary evidence, decisive criteria,
and the recommended path visible. These are semantic tasks, not required chapters or
layouts.

## 证据规则

- Bind every material benefit, cost, feasibility claim, risk, and constraint to an
  eligible source, or mark it as an assumption, projection, inference, simulation, or
  pending verification under the existing disclosure rules.
- Keep criterion definition and weight provenance visible. An Agent-proposed weight
  is not a customer preference or source fact.
- Preserve limiting and refuting evidence alongside supporting evidence. Never
  disguise a preferred option as the only option or present projected outcomes as
  achieved results.
- Treat eliminated options as auditable decision history when their removal affects
  the conclusion. State the reason and what evidence could reopen them.
- Do not use stronger recommendation language than the evidence supports. A stage-ready
  visual or confident tone cannot raise evidence strength.
- Apply the existing high-risk verification and source-protection rules without
  relaxation. Ordinary creative supplements remain usable only with delivery-time
  disclosure and adjacent labels where the shared contract requires them.

## 横向参数默认值

- `input_entry_route`: inherit the established material route
- `use_mode`: `reading` recommendation only after explicit delegation; otherwise inherit or resolve the existing startup choice
- `visual_binding`: inherit the validated visual route
- `evidence_rigor`: `standard`
- `information_density`: `medium`
- `motion_density`: `minimal` recommendation only; require customer selection or explicit delegation
- `continuation_state`: inherit the Handoff decision

These defaults never override a known, confirmed, inherited, or explicitly delegated
horizontal value. `content_length` remains the shared independent choice.

## IR 映射边界

Direct HTML remains the default. Only when the IR engineering route is independently authorized
may this Profile guide existing `claim`, `evidence`,
`comparison`, `process`, and `narrative_unit` semantics, plus existing page task,
relationship, and Visual Intent combinations.

Do not add a proposal or decision field to the Report IR Schema. Do not create a
scoring engine, decision algorithm, fixed JSON decision model, arbitrary HTML/CSS/JS,
Compiler branch, or Profile-triggered IR path. The customer-readable decision state
belongs in the confirmed Report Design Brief; any authorized IR remains downstream.

## Runtime/主题使用

Use the confirmed reading or presentation mode, current Runtime contract, and the
validated built-in/project-theme route. Comparison emphasis or staged explanation may
use existing page composition and `fragment-v1` only when the confirmed mode and
actual narrative need it.

The Profile does not add complex composition, cross-page morphing, decision widgets,
new interaction state, incremental compilation, or a theme implementation. Do not
turn a visual comparison into an unsupported interactive scoring tool.

## QA 验收

Run all existing objective QA, Runtime/editor checks where applicable, traceability,
asset/browser QA, authorization rechecks, Handoff validation, and delivery gates. In
addition, verify:

- the decision, decision maker, urgency, boundary, and no-decision consequence are
  clear;
- the option set is real for the claimed comparison and exposes provenance,
  disposition, meaningful status quo, and known omissions;
- criteria and weights have stable meanings and are applied consistently rather than
  reverse-engineered for the result;
- facts, assumptions, projections, evidence strength, contrary evidence, and unknowns
  remain distinguishable;
- cost, benefit, risk, reversibility, implementation conditions, and material
  trade-offs are visible without implying false precision;
- the recommendation is traceable to criteria, evidence, and explicit trade-offs,
  with premises, failure conditions, and residual risks;
- implementation steps, responsible owners, resource/time boundaries, and the next
  decision are explicit; and
- an external-action promise, when present, uses the exact existing verified action
  path and matches its source and final display.

Any failure remains a Profile-specific QA failure in addition to the shared gate; it
does not replace or collapse the existing QA and delivery conclusions.

## 能力叠加与冲突处理

Research support, operating data, teaching explanation, or live delivery may be
bounded overlays with a stated source Profile, reason, and affected scope. They may
not import another Profile's full intake, design-ready gate, narrative sequence,
artifact set, or QA workflow.

If the primary success condition becomes spoken audience persuasion, switch the
primary Profile to `live-presentation-persuasion`, rebuild only affected design
decisions, and use the existing complete-brief confirmation. Never run both Golden
Paths as full workflows.
