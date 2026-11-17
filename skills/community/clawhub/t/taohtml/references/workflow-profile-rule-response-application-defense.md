# 规则响应、申报与答辩

## 身份与版本

- `profile_id`: `rule-response-application-defense`
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

Use as primary only when success is materially governed by an authoritative
eligibility, application, tender, procurement, grant, award, review, scoring,
evaluation, submission, or defense rule and the artifact must make compliance and
score-bearing responses independently checkable.

The authority, applicable rule identity/version, and real effect on acceptance must
be established semantically. A rule file's presence, a submission label, a formal
tone, `presentation` use mode, or the fact that reviewers will read the artifact does
not by itself select this Profile.

## 排除范围

Do not use as primary for ordinary formal writing without governing qualification,
mandatory-response, scoring, or defense rules. Use
`formal-submission-writing` when institutional recipient/use/archival correctness is
dominant but no authoritative rule set decides success.

Do not select this Profile for a general speech or pitch whose audience movement is
not controlled by declared application or review criteria. Do not create a fixed
compliance schema, customer questionnaire, scoring algorithm, mandatory matrix,
chapter directory, page count, table/card template, or rule parser.

## 成品

Depending on the confirmed objective and proof state, produce one of two honestly
named customer-usable results through the existing TaoHtml chain:

- a formal offline submission or defense artifact whose actual mandatory and score-
  bearing requirements are covered, evidenced, and locatable; whose mandatory proof
  is sufficient; whose actual TaoHtml deliverable format/package is accepted by the
  applicable submission channel; and whose deadline and every other mandatory
  submission constraint are actually satisfied; or
- an explicitly requested `gap-analysis / preparation draft` that maps requirements,
  available responses, missing proof, conflicts, owners, and submission risk, while
  stating clearly that it is not a compliant submit-ready final artifact.

Both results retain current-file Production Authorization, direct-HTML production,
the existing Runtime/theme routes, objective QA, Handoff, and
`《待核实内容清单》`. There is no required chapter count, page count, response table,
card system, or defense layout independent of the real rule set.

## 所需信息

Reuse eligible conversation, bound sources, the confirmed Material Understanding
Summary, and still-supported Handoff state before identifying a gap. Maintain the
shared `known | confirmed | inferred | missing` ledger; do not expose the following
as a Profile form or ask the user to fill a matrix.

### 规则身份与检查状态

Bind the governing rule before claiming coverage:

- publishing/issuing authority and, when different, the receiving or review body;
- exact document, notice, specification, invitation, guideline, or rule identity;
- applicable version, edition, amendment, effective date or period, and supersession
  status when supplied by authority;
- submission, clarification, evaluation, or defense deadline as applicable; and
- exact checked scope, including inspected sections, appendices, forms, amendments,
  Q&A/clarifications, and any explicitly unavailable part.

`文件存在` does not mean `规则已核验`. A filename, cached copy, prior summary, or
current artifact cannot establish applicability, completeness, or current version
without the required source binding and inspection record.

### 规则类别状态

Identify only categories the actual applicable rule contains:

- `资格/一票否决项`: entry conditions, exclusions, disqualifiers, or pass/fail
  thresholds;
- `强制响应项`: content, declaration, proof, signature, form, or attachment that
  must be supplied;
- `评分项与权重`: declared review dimensions, points, weights, formula, or scoring
  interpretation;
- `加分项`: explicitly declared optional credit or preference;
- `格式/篇幅/提交约束`: structure, page/word/character limit, file/package, naming,
  medium, copies, deadline, submission channel, or other delivery constraint; and
- `答辩要求`: presentation, question, duration, speaker, demonstration, device, or
  evidence-use requirement.

Do not invent a category merely because it is common in similar applications. When
the rule supplies no score, weight, bonus, veto, or defense requirement, record that
the category is not present or not established rather than filling it synthetically.

### 响应—证据状态

For every actual requirement, keep a traceable project-local relationship that the
Agent can audit and the final artifact can express as appropriate:

- original wording or accurate paraphrase plus rule locator;
- response content;
- supporting evidence and evidence locator;
- responsible owner;
- current status;
- gap, conflict, or dependency; and
- final presentation location in the submission or defense artifact.

Use honest customer-readable status language such as `已满足`, `部分满足`,
`缺少证明`, `冲突`, `待确认`, or `不适用`. Evidence availability and requirement
satisfaction are separate: possessing a document, certificate image, case file, or
draft response does not justify `已满足` until the exact requirement and proof are
checked.

This relationship is Profile judgment and a project-local working record, not a new
TaoHtml Schema, fixed JSON contract, required matrix deliverable, or user form. Choose
the record and presentation shape that fits the actual rule and project.

### 最大缺口规则

After each pass, ask at most the one largest still-missing item whose answer could
change eligibility, mandatory coverage, score-bearing meaning, proof sufficiency,
actual deliverable format/channel compatibility, deadline viability, submission
legality, responsibility, or the claimed deliverable class. Reuse the shared 0-6
question budget, repetition rule, information-gain stop, and hard boundaries; do not
add a Profile questionnaire or independent confirmation round.

Do not spend the question budget collecting every row manually when eligible material
already contains the answer. Ordinary expression and non-proof examples may follow
the shared output-first path. A missing mandatory proof is not an ordinary gap
eligible for creative supplements. Neither is an unsupported required format/package,
an incompatible mandatory submission channel, a missed deadline, or another
unsatisfied mandatory submission constraint.

## design-ready 条件

The shared design-ready gate must pass, plus the rule response must have a truthful
basis appropriate to its confirmed deliverable class.

For a formal submission or compliance-ready defense, require:

- publishing authority, rule/document identity, applicable version/effective basis,
  deadline, and checked scope;
- actual eligibility/veto, mandatory response, scoring/weight, bonus, format/
  submission, and defense categories identified only where present;
- every actual requirement represented by a response-evidence status and final
  presentation location;
- qualification, score-bearing claims, credentials, commitments, customers,
  performance, completed results, and compliance conclusions supported at their real
  evidence strength;
- `actual deliverable format/channel compatibility`: the exact TaoHtml output format
  and package are accepted by the applicable submission channel without assuming an
  unsupported export, conversion, packaging, or submission capability;
- the applicable deadline and every other mandatory submission constraint that
  decides whether the actual artifact can be submitted are already satisfied;
- responsibility owners, unresolved conflicts, and submission risks visible; and
- no missing mandatory proof or unsatisfied mandatory submission constraint that
  would make a compliance or submit-ready claim false.

When mandatory proof is missing, the actual TaoHtml format/package is not accepted by
the mandatory channel, the deadline cannot be met, or any other mandatory submission
constraint is unsatisfied, do not fabricate eligibility or a compliant final
artifact. Block as needed, or continue only if the user explicitly changes the
requested result to `gap-analysis / preparation draft`. That diagnostic branch may
become design-ready after its inspected scope, known gaps, owners, risks, and non-
submit-ready boundary are clear. It still uses the existing complete-brief
confirmation, current-file Production Authorization, QA, delivery, and Handoff rules;
it must never be labeled as a compliant submission. Do not add an output-format,
conversion, packaging, channel-submission, or deadline-bypass capability to escape
this boundary.

### 设计简报增量

Write these customer-readable fields inside the one existing Report Design Brief's
adaptive `场景特有决策` section. Reuse the current ledger; do not create a second
brief, Profile questionnaire, or Profile-specific confirmation round.

- `规则身份与版本`: publishing authority, rule/document identity, applicable
  version/effective basis, deadline, checked scope, and unavailable parts;
- `申报/评审目标`: application, tender, award, evaluation, submission, or defense
  goal and whether the deliverable is formal or `gap-analysis / preparation draft`;
- `资格与强制项`: actual eligibility/veto and mandatory response requirements,
  locators, owners, and present status;
- `评分与权重`: only declared score-bearing items, points/weights/formula, source
  locators, and unresolved interpretation;
- `响应—证据状态`: requirement, response, proof, both locators, owner, honest status,
  gap/conflict, and planned output location at the level useful to the project;
- `格式/截止/答辩约束`: actual format, length, package, channel, deadline, defense,
  speaker/device, and interaction constraints;
- `责任边界`: who supplies, verifies, approves, signs, submits, presents, and owns
  each unresolved requirement; and
- `缺口/冲突与提交风险`: missing mandatory proof, incompatible actual deliverable
  format/package/channel, missed or unsatisfied deadline, other mandatory submission
  constraints, rule conflict/version uncertainty, unsupported score claims,
  unresolved responsibility, and impact on submit-ready status.

Record reversible inferences and their bases in the existing `待确认项`. Display and
confirm the complete current brief once. Profile selection, complete-brief
confirmation, and current-file Production Authorization remain three independent
facts.

## 叙事任务

### Golden Path

1. **Enter through shared state.** Establish or inherit the material route, task
   intent, use mode, content length, source bindings, and exactly one primary Profile
   under the shared contracts. Do not route here from a formal document or
   presentation mode alone, and do not reopen known choices.
2. **Bind and inspect the governing rule.** Record publisher, rule/document identity,
   applicable version/effective basis, deadline, and exact checked scope. Distinguish
   an available file from a verified applicable rule, and ask only the current
   largest result-changing gap when one remains.
3. **Classify only actual requirements.** Separate eligibility/veto, mandatory
   responses, scoring/weights, bonuses, format/submission constraints, and defense
   requirements only where the rule establishes them. Preserve original wording or
   an accurate paraphrase and exact locator; never back-fit or rewrite a rule to make
   a response appear stronger.
4. **Build requirement-response-evidence traceability.** For every actual requirement,
   connect rule text/locator, response, evidence/locator, owner, honest status,
   gap/conflict, and final presentation location. A file's existence is evidence
   availability, not automatic satisfaction.
5. **Choose the honest deliverable branch.** Build a formal compliant or submit-ready
   response only when mandatory proof is sufficient, the actual TaoHtml deliverable
   format/package is accepted by the applicable submission channel, and the deadline
   plus every other mandatory submission constraint is actually satisfied. If any
   condition fails, block a compliant or submit-ready claim; proceed only after the
   user explicitly requests a `gap-analysis / preparation draft`, and make its
   diagnostic, non-submit-ready boundary visible from brief through delivery.
   Disclosure records the failure; it does not satisfy the constraint or make the
   artifact submit-ready.
6. **Design for reviewer verification and scoring.** Sequence content so the reviewer
   can locate each applicable response and proof, follow declared scoring logic, see
   differentiators at their real evidence strength, and find gaps without hunting.
   Derive the directory, pages, tables, or prose from the actual rule and material;
   do not force a fixed outline, page count, matrix, or card layout.
7. **Prepare the rule-bound defense when applicable.** Keep this Profile primary and
   add live-presentation capability only as a bounded overlay. Align oral claims,
   visible proof, expected rule-bound questions, and the final page with the same
   response-evidence state; do not overclaim beyond the written evidence.
8. **Use the one shared brief and authorization chain.** Add only the fields above to
   the current Report Design Brief, obtain its ordinary complete-brief confirmation,
   then pass current-file Production Authorization. Do not add another confirmation
   or treat a rule mapping as formal-production permission.
9. **Produce through the existing chain.** After authorization, follow
   `process-playbook.md`, save the first runnable direct-HTML artifact, apply the
   validated visual route and current Runtime, then run specialized plus shared QA
   and delivery gates.

### 页面任务与评审核验重点

Derive page and section roles from the actual rule. Useful semantic jobs may include
rule identity/scope, eligibility, mandatory response, score-bearing claim, proof,
differentiator, gap/conflict, submission constraint, defense question, and closure.
Make the response and its evidence locator visible where a reviewer expects to verify
it. These are semantic tasks, not required chapters, fixed tables, cards, or pages.

## 证据规则

- Bind every eligibility statement, veto condition, mandatory response, point/weight,
  bonus, credential, certificate, customer, achievement, commitment, completed result,
  citation, and compliance conclusion to the applicable rule and eligible evidence.
- Never invent a score, weight, qualification, certificate, customer, performance,
  commitment, completed result, citation, proof locator, or compliance status. Visual
  confidence and reviewer-friendly ordering cannot upgrade evidence strength.
- Preserve rule wording and meaning. Use an accurate paraphrase only when its locator
  remains available; never reverse-engineer the rule, hide an adverse clause, change
  a scoring basis, or reinterpret a mandatory item to fit available material.
- Keep `已满足`, `部分满足`, `缺少证明`, `冲突`, `待确认`, and `不适用` honest. Do not
  convert `有文件`, `已起草`, or `计划取得` into satisfaction.
- Preserve contrary evidence, expired or wrong-version proof, name/entity mismatch,
  missing signatures, unavailable attachments, and owner conflicts when they affect
  eligibility, score, or submission risk.
- Treat acceptance of the actual deliverable format/package/channel and satisfaction
  of the deadline and other mandatory submission constraints as verifiable rule
  conditions. A locally openable HTML or successful current-file Production
  Authorization does not prove channel acceptance or external submit-ready status.
  Do not invent conversion, export, packaging, submission, or deadline-bypass
  capabilities. Disclosure of incompatibility records a gap; it never satisfies it.
- A gap-analysis or preparation draft may organize unresolved proof but may not use
  creative completion to simulate official evidence, achieved results, credentials,
  signatures, or compliant completion.
- Apply the shared source-role/availability, external-evidence verification, high-risk
  fact, output-first, and `《待核实内容清单》` rules without weakening the mandatory-
  proof boundary.

## 横向参数默认值

- `input_entry_route`: inherit the established material route
- `use_mode`: `reading` recommendation only after explicit delegation; otherwise inherit or resolve the existing startup choice
- `visual_binding`: inherit the validated visual route
- `evidence_rigor`: `formal`
- `information_density`: `high`
- `motion_density`: `minimal` recommendation only; require customer selection or explicit delegation
- `continuation_state`: inherit the Handoff decision

These defaults never override a known, confirmed, inherited, or explicitly delegated
horizontal value. `content_length` remains the shared independent choice. A defense
does not silently replace a known use mode or motion density.

## IR 映射边界

Direct HTML remains the default. Only when the IR engineering route is independently
authorized may this Profile guide existing `claim`, `evidence`, `source`,
`comparison`, appendix, citation, presentation Projection, page-task, and
`narrative_unit` semantics.

Do not add qualification, compliance, rule-response, score, weight, certificate,
owner, or requirement-status fields to the Report IR Schema. Do not create a fixed
JSON compliance model, scoring engine, rule parser, Profile-triggered IR path, or
Compiler branch. The customer-readable rule/response state belongs in the confirmed
Report Design Brief and project-local record; any authorized IR remains downstream.

## Runtime/主题使用

Use the established reading mode for a submission or presentation mode for a defense
only after the shared use-mode decision. Theme and visual binding remain independent
and cannot change rule meaning, evidence strength, or compliance status.

For a defense, use only the current single-screen Runtime and existing `fragment-v1`
semantics for monotonic reveal, grouped steps, focus, whole-page navigation, reverse
steps, and per-page return state. Do not promise dual-screen presenter view,
speaker-notes UI, cross-page morphing, complex state, new controls, or a new Runtime.

## QA 验收

Run all existing objective QA, traceability, asset/browser QA, current-file
authorization rechecks, Handoff validation, and delivery gates. In addition, verify:

- the publishing authority, rule/document identity, applicable version/effective
  basis, deadline, amendments, and exact checked scope are correct and current for
  the claimed result;
- `mandatory coverage`: every actual eligibility/veto and mandatory response item has
  a rule locator, response, owner, honest status, output location, and required proof
  or an explicitly blocking gap;
- every score-bearing claim is supported by eligible evidence at its actual strength,
  with exact evidence location and no invented qualification, certificate, customer,
  achievement, commitment, or completed result;
- points, weights, formulas, totals, and repeated scoring references match the
  authoritative rule and remain internally consistent; categories absent from the
  rule have not been created;
- every rule locator, evidence locator, response location, appendix/attachment
  reference, and final output location resolves accurately;
- for a formal compliant or submit-ready result, the actual delivered format/package
  is accepted by the applicable submission channel, the mandatory length,
  page/word/character, naming, copy, and defense constraints are actually satisfied,
  and the real submission can still occur within the mandatory deadline; none may
  pass merely by being disclosed;
- disclosure in the artifact, risk list, delivery note, or Handoff records an
  unsatisfied mandatory constraint; disclosure does not make the artifact compliant
  or submit-ready;
- missing proof, partial satisfaction, conflict, pending confirmation, inapplicability,
  expired/wrong-version proof, and unresolved responsibility are disclosed rather
  than upgraded or hidden;
- when mandatory proof, actual format/package/channel compatibility, deadline, or any
  other mandatory submission constraint is unsatisfied, the result is blocked or the
  user has explicitly reclassified it as `gap-analysis / preparation draft`; that
  diagnostic draft may disclose the unsatisfied items but is labeled throughout as
  not a compliant submit-ready artifact, including its delivery wording and Handoff;
  and
- defense final pages, staged intermediate states, speaker-support content, and oral
  wording do not exceed the verified written response or evidence, while exact
  `fragment-v1` navigation and target viewports pass the current Runtime QA.

Any failure remains a Profile-specific QA failure in addition to the shared gate; it
does not replace or collapse existing QA and delivery conclusions.

## 能力叠加与冲突处理

Formal writing, research support, decision explanation, and live delivery may be
bounded overlays with a stated source Profile, reason, and affected scope. They may
not import another Profile's complete intake, design-ready gate, narrative sequence,
artifact set, or QA workflow.

Keep this Profile primary through both written response and rule-bound defense when
authoritative qualification, mandatory response, scoring, or defense rules determine
success; use `live-presentation-persuasion` only as a bounded overlay. When those rules
do not decide success, route to the actual dominant business outcome—ordinary formal
submission uses `formal-submission-writing`, while a general talk may use the live
Profile. Never run two complete Golden Paths simultaneously.
