# 研究分析与专业论证

## 身份与版本

- `profile_id`: `research-analysis-argumentation`
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

Use as primary only when the artifact's main job is to answer a substantive question,
test or bound a hypothesis, explain a mechanism, or form a professional conclusion
whose method, evidence, reasoning, and limits must remain inspectable.

Select this Profile from the real question and required conclusion strength. Many
citations, professional tone, data charts, an appendix, or a research-style filename
do not by themselves establish a research objective.

## 排除范围

If the main outcome is to make a responsible person choose or approve an option, use
`proposal-planning-decision`. If authoritative qualification, mandatory-response,
scoring, or defense rules determine success, use
`rule-response-application-defense`. If the artifact only explains performance for a
recurring operating period, use `periodic-operations-reporting`.

Do not create a fixed research-report directory, paper template, page count, research
questionnaire, scoring algorithm, literature form, Claim table, card system, or
mandatory appendix. Research validity comes from the actual method and evidence, not
from a familiar document shape.

## 成品

A customer-usable offline HTML professional analysis that can be read independently
or presented under the already confirmed `use_mode`, and that makes the following
traceable at the strength actually achieved:

- the substantive question, decision context, terms, scope, and intended conclusion
  strength;
- methods actually used, material/data checked, missing coverage, transformations,
  and limitations;
- Claim–Evidence–Source relationships, competing explanations, conflicts, and
  counterevidence;
- reasoning from observations to bounded conclusions, including causal limits; and
- limitations, next validation steps, unresolved items, standard QA evidence,
  Handoff, and `《待核实内容清单》`.

The result has no required chapter count, page count, thesis format, or journal
structure. Its delivery class must remain honest: a provisional analysis is not a
validated final study merely because the HTML is polished.

## 所需信息

Reuse eligible conversation, bound sources, the confirmed Material Understanding
Summary, and still-supported Handoff state before identifying any gap. Maintain the
shared `known | confirmed | inferred | missing` ledger; do not expose the following as
a separate research questionnaire.

### 研究边界与结论强度

Resolve only what is necessary to judge the analysis honestly:

- the research question and the audience's decision or professional-use context;
- the analysis object and applicable time, geography, population, sample, segment,
  system, or other scope boundary;
- core terms, metric/data definitions, classification rules, and interpretive basis;
- the conclusion strength required, such as exploratory orientation, supported
  inference, mechanism explanation, prediction, or a formal professional conclusion;
  and
- which result would change a decision, reject a hypothesis, or require a different
  method.

Do not silently generalize a result outside the inspected population, period,
location, sample, or applicability boundary.

### 方法与检查状态

Keep proposed work distinct from completed work. Record:

- methods actually used and their execution status;
- methods only planned, proposed, described by a source, or not completed;
- data and material identity/version, inspected scope, sampling or selection basis,
  and missing scope;
- transformations, calculations, coding/classification decisions, checks, and
  reproducibility limits; and
- method assumptions, limitations, conflicts, and failure conditions.

Never write a planned interview, survey, experiment, literature review, comparison,
model, or calculation as though it was performed. File availability, a method section,
or an earlier summary does not prove method completion.

### 主张与推理状态

Use customer-readable distinctions throughout working records, the brief, pages, and
delivery:

- `观察/事实 (observation / fact)`: directly observed or supported within the stated
  inspection boundary;
- `推论 (inference)`: reasoned from stated evidence and assumptions;
- `假设 (hypothesis)`: a testable explanation not yet established;
- `推演/模拟 (projection / simulation)`: a modeled or scenario-dependent result;
- `建议 (recommendation)`: a proposed action rather than a finding; and
- `未决冲突 (unresolved conflict)`: incompatible evidence, definitions, methods,
  or interpretations that could change the conclusion.

Track the target Claim, its supporting/limiting/refuting/background evidence, source,
relationship strength, and current conclusion boundary. A single evidence item may
relate to several Claims, but each relationship must state its honest role and
strength.

### 最大缺口规则

After each pass, ask at most the one largest still-missing item whose answer could
reverse the conclusion, invalidate the method, change the scope, or make the claimed
conclusion strength false. Reuse the shared 0-6 question budget, repetition rule,
information-gain stop, and hard boundaries; do not add a research intake cycle.

Ordinary expression and low-risk structure gaps may follow output-first production.
Critical facts, source identity, method completion, sample, data, calculations,
formal findings, quotations, citations, surveys, interviews, experiments, and
research outcomes may not be creatively completed.

## design-ready 条件

The shared design-ready gate must pass, plus the following research decisions must be
sufficiently clear for the honest delivery class:

- question, audience/decision context, object, scope, core terms, definitions, and
  target conclusion strength;
- methods actually completed versus planned, data/material coverage, missing scope,
  and material method limitations;
- the core Claim–Evidence–Source state, source versions/times, inspection coverage,
  claim-fit, conflicts, and evidence gaps;
- observation/fact, inference, hypothesis, projection/simulation, recommendation,
  and unresolved-conflict boundaries;
- relevant counterevidence, alternative explanations, mechanism evidence, causal
  identification boundary, and next validation need; and
- the exact formal or provisional delivery wording that the evidence can support.

A formal professional conclusion is design-ready only when method execution,
evidence, and claim-fit reach the claimed strength. When critical evidence is
insufficient, do not pretend verification is complete. Block the formal conclusion,
or continue only after the user explicitly accepts an exploratory/preliminary scope.
That branch may become design-ready when its checked scope and limitations are clear,
but `provisional | exploratory | preliminary` status must remain visible in the
brief, every conclusion-bearing page, delivery wording, and Handoff. It must not be
packaged as a validated final study.

### 设计简报增量

Write these customer-readable fields inside the one existing Report Design Brief's
adaptive `场景特有决策` section. Reuse the current ledger; do not create a second
brief, research form, or independent confirmation. Do not add a Profile-specific confirmation round.

- `研究问题与决策语境`: substantive question, intended audience/use, and what
  the analysis may change;
- `范围与术语口径`: object, time/geography/population/sample/applicability,
  core definitions, units, and classification basis;
- `方法与已检查材料`: methods actually used, execution status, data/material
  versions, checked and missing scope, transformations, and limitations;
- `核心 Claim–Evidence 状态`: material Claims, linked evidence/sources,
  relationship role and strength, source location, and claim-fit;
- `替代解释/冲突`: competing explanations, counterevidence, unresolved
  conflicts, and causal-identification boundary;
- `目标结论强度`: requested and currently supportable strength, including
  formal or provisional status;
- `关键局限/缺口`: missing evidence, sample/method limits, unavailable checks,
  and what could overturn the result; and
- `交付边界`: independent-reading or confirmed-presentation use, conclusion
  labels, unresolved items, next validation, and what the artifact does not establish.

Record reversible inferences and their bases in the existing `待确认项`. Display and
confirm the complete current brief once. Profile selection, complete-brief
confirmation, and current-file Production Authorization remain three independent
facts.

## 叙事任务

### Golden Path

1. **Enter through shared state.** Establish or inherit the material route, task
   intent, use mode, content length, source bindings, and exactly one primary Profile.
   Do not route here from citations, tone, or charts alone, and do not reopen known
   horizontal values.
2. **Bind the real question and boundary.** Make the question, audience/decision
   context, analysis object, scope, terms, and required conclusion strength explicit.
   Ask only the current largest result-changing gap when one remains.
3. **Audit actual method and coverage.** Separate completed from planned methods;
   record data/material versions, checked and missing scope, units, selection or
   sample basis, transformations, calculations, conflicts, and limitations. Never
   convert a plan into a completed study.
4. **Build Claim–Evidence–Source traceability.** Connect each material Claim to exact
   evidence and source locations, record relationship role/strength and claim-fit,
   and preserve items that limit, refute, or merely contextualize the Claim. A file's
   existence is never treated as fact verification.
5. **Test competing explanations.** Seek relevant counterevidence, alternative
   explanations, scope failures, and unresolved conflicts. Distinguish correlation,
   mechanism evidence, and causal identification; without causal identification,
   never state that causation has been proved.
6. **Reason to an honest branch.** Derive observations, inferences, hypotheses,
   projections/simulations, recommendations, and bounded conclusions at their real
   strength. If the formal branch fails, block it or use only the explicitly accepted
   provisional branch, preserving that boundary through pages and Handoff.
7. **Build the research sequence from the question.** Usually complete the jobs of
   question and boundary → method and evidence basis → key observations → competing
   explanations/counterevidence → reasoning → bounded conclusion → limitations and
   next validation. Use only the jobs the actual analysis needs; do not turn this
   sequence into a fixed chapter template.
8. **Use the one shared brief and authorization chain.** Add only the fields above to
   the current Report Design Brief, obtain its ordinary complete-brief confirmation,
   then pass current-file Production Authorization. Do not add another confirmation
   or treat Profile selection as production authority.
9. **Produce through the existing chain.** After authorization, follow
   `process-playbook.md`, save the first runnable direct-HTML artifact, apply the
   validated visual route and current Runtime, then run specialized plus shared QA
   and delivery gates.

### 页面任务与研究表达

Give each page one real research job, such as defining the question, establishing a
method, proving or limiting a Claim, comparing explanations, synthesizing reasoning,
stating a bounded conclusion, or exposing limitations. Put evidence or its exact
locator where the relevant Claim can be checked. These are semantic jobs, not fixed
chapters, cards, tables, diagrams, or page layouts.

Page text may be concise for a confirmed presentation mode, but the evidence chain
may not disappear. Put complete support in visible sources, appendices, evidence
modals, or speaker support only through existing mechanisms, and keep it traceable.

## 证据规则

- Maintain real Claim–Evidence–Source relationships for every material conclusion.
  File existence is not fact verification; a secondary summary is not automatically
  original evidence; source credibility is not proof that the source fits the
  current Claim.
- Record source identity/version/time, exact locator, inspection coverage, applicable
  scope, and what the source can and cannot establish. For data, also record unit,
  definition, time/geography/sample range, method, transformations, calculations,
  and conflicts.
- Inspect supporting evidence together with limitations, counterevidence, and
  alternative explanations. Do not collect only material that confirms the initial
  conclusion or silently omit a disconfirming result.
- Distinguish correlation, mechanism evidence, and causal conclusions. Correlation
  or timing alone cannot be upgraded to proved causation.
- One evidence item may serve several Claims, but each relationship must honestly say
  whether it supports, limits, refutes, or supplies background and at what strength.
- Short page copy never waives the evidence chain. Complete evidence may move to a
  source/appendix/evidence modal or supported speaker material, but the Claim and
  locator must still resolve.
- Never invent data, samples, interviews, surveys, experiments, methods performed,
  research results, sources, citations, quotations, calculations, or authoritative
  endorsements. Never call planned or incomplete work completed.
- Apply the shared source-role/availability, external-evidence verification,
  high-risk, output-first, and `《待核实内容清单》` rules without weakening these
  hard boundaries.

## 横向参数默认值

- `input_entry_route`: inherit the established material route
- `use_mode`: `reading` recommendation only after explicit delegation; otherwise inherit or resolve the existing startup choice
- `visual_binding`: inherit the validated visual route
- `evidence_rigor`: `formal`
- `information_density`: `high`
- `motion_density`: `minimal` recommendation only; require customer selection or explicit delegation
- `continuation_state`: inherit the Handoff decision

These defaults never override a known, confirmed, inherited, or explicitly delegated
horizontal value. `content_length` remains the shared independent choice. An accepted
provisional branch may lower the actually supportable evidence posture without
silently changing the user's other horizontal parameters.

## IR 映射边界

Direct HTML remains the default. Only when the IR engineering route is independently
authorized may this Profile guide existing research prototype, evidence rigor,
`claim`, `evidence`, `source`, dataset, appendix, citation, `narrative_unit`, page-task,
and Projection semantics.

Do not add research-question, method-completion, sample, causal-status, provisional-
result, or Claim–Evidence relationship fields to the Report IR Schema. Do not create a
fixed JSON research model, literature database, research scoring algorithm,
Profile-triggered IR path, Compiler branch, or Validator bypass. The customer-readable
research state belongs in the confirmed Report Design Brief and project-local working
record; any authorized IR remains downstream.

## Runtime/主题使用

Use only the established reading or presentation mode, validated built-in/project/
enterprise visual route, and current Runtime. Existing source modals, page semantics,
and `fragment-v1` may support evidence inspection or spoken order when the confirmed
mode requires them.

The Profile does not add a research theme, citation engine, dual-screen presenter
view, speaker-notes UI, cross-page morphing, complex state, live data, or new Runtime
controls. Theme and motion cannot increase Claim strength or imply authority.

## QA 验收

Run all existing objective QA, traceability, asset/browser QA, current-file
authorization rechecks, Runtime/editor checks where applicable, Handoff validation,
and delivery gates. In addition, verify:

- `question-to-conclusion`: the final conclusion answers the stated question inside
  the declared object, scope, terms, and conclusion-strength boundary;
- `method-to-result`: every result attributed to a method was actually produced by
  that completed method, with checked/missing scope and limitations visible;
- `Claim–Evidence–Source`: material Claims resolve to the intended evidence and exact
  source location, with relationship role, strength, and claim-fit recorded;
- source identity/version/time, applicability, checked scope, data units,
  definitions, period/geography/sample, transformations, and calculations are
  correct and repeated consistently;
- observation/fact, inference, hypothesis, projection/simulation, recommendation,
  and unresolved-conflict labels agree across titles, visuals, body text, sources,
  and conclusions;
- correlation, mechanism evidence, and causal conclusions remain distinct, and no
  claim says causation was proved without adequate identification;
- counterevidence, alternative explanations, conflicts, missing scope, and material
  limitations remain visible rather than hidden by summary or stagecraft;
- conclusion strength never exceeds the completed method, evidence, or claim-fit;
  exploratory/preliminary results remain non-final throughout pages, delivery wording,
  and Handoff; and
- no file's existence, polished citation, or secondary summary is treated as proof of
  a verified fact or completed research step.

Any failure remains a Profile-specific QA failure in addition to the shared gate; it
does not replace or collapse existing QA and delivery conclusions.

## 能力叠加与冲突处理

Decision framing, periodic data context, formal writing, teaching explanation, or
live delivery may be bounded overlays with a stated source Profile, reason, and
affected scope. They may not import another Profile's complete intake, design-ready
gate, narrative sequence, artifact set, or QA workflow.

Keep this Profile primary while the method-and-evidence-backed answer remains the
dominant product. If the main result becomes a choice among options, switch to
`proposal-planning-decision`; if authoritative rules decide success, switch to
`rule-response-application-defense`; if the work only explains a recurring operating
period, switch to `periodic-operations-reporting`. Rebuild only affected decisions,
reuse the existing complete-brief confirmation, and never run two Golden Paths in
full.
