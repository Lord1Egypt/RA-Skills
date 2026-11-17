# 教学培训与知识传递

## 身份与版本

- `profile_id`: `teaching-training-knowledge-transfer`
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

Use as primary only when the artifact's main job is to help a defined learner group
acquire, understand, retain, practice, or apply specific knowledge, a method, or a
skill, and the learning path must make that transfer possible within an honest
completion boundary.

Select this Profile from the target learner performance and learning-transfer
outcome. “Make a training PPT”, the presence of an instructor, content that needs
explanation, or `presentation` use mode does not by itself establish this Profile.

## 排除范围

If the main result is audience agreement, approval, purchase, or another persuasive
action, use `live-presentation-persuasion` or
`brand-communication-editorial-publishing` according to the dominant delivery
condition. If the main result is a method-and-evidence-backed professional conclusion,
use `research-analysis-argumentation`. Teaching explanation inside another Profile
is only a bounded capability overlay.

Do not create a fixed course chapter count, page count, instructional method, Bloom
level, lesson plan, card system, question type, classroom flow, assessment form, or
course questionnaire. Do not implement an LMS, quiz engine, automatic scoring,
learner state, completion tracking, certificate system, or training database.

## 成品

A customer-usable offline HTML course or training artifact that can be read or
presented under the already confirmed `use_mode`, and that contains:

- a learning progression derived from the target capability and prerequisite state;
- accurate concepts, methods, steps, examples, misconceptions, and failure modes;
- practice, judgment, or review only where it serves the actual goal and current
  capabilities can support it;
- instructions, answers, feedback, or open-response boundaries that agree with one
  another;
- a truthful statement of what the artifact teaches, supports, and does not prove;
  and
- the existing current-file authorization, objective QA, Handoff, delivery, and
  `《待核实内容清单》` boundaries.

The result has no required course length, chapter count, page count, exercise count,
teaching method, or classroom sequence. A complete artifact does not by itself prove
that any learner has attended, mastered, passed, been certified, or achieved a
learning effect.

## 所需信息

Reuse eligible conversation, bound sources, the confirmed Material Understanding
Summary, and still-supported Handoff state before identifying a gap. Maintain the
shared `known | confirmed | inferred | missing` ledger; do not expose the following
as a separate course questionnaire or fixed lesson-planning form.

### 学习者、目标能力与范围

Resolve only what is needed to design the real learning path:

- learner group and relevant differences that materially affect instruction;
- existing baseline, prerequisite knowledge, prior experience, and likely vocabulary;
- target capability and observable performance in the intended application context;
- the situations in which the learner must use, explain, judge, or perform the
  knowledge or method;
- instructional scope, depth, exclusions, and any responsibility or safety boundary;
  and
- the distinction between having seen or heard something, understanding it, being
  able to explain it, being able to perform it, and applying it in context, without
  forcing those states into a fixed taxonomy.

Do not convert a broad topic label into a claim that learners will be able to perform
a task. State the target at the level the source, time, support, and practice boundary
can honestly sustain.

### 知识依赖、示例与误解状态

Map the parts that can change progression or practice:

- concept, rule, procedure, or skill dependencies and the order in which prerequisites
  must become available;
- correct examples, worked examples, counterexamples, failure modes, and common
  misconceptions;
- which example is a real sourced case, a customer-provided example, an editorially
  simplified example, or an explicitly illustrative learning situation;
- high-risk knowledge, operational steps, safety/compliance points, and the source
  strength required before teaching them as fact or guidance; and
- what feedback is needed to correct an error rather than merely reveal an answer.

A polished explanation does not establish that a factual rule or operational step is
correct. An illustrative exercise may teach a distinction, but it cannot become a
real customer case, learner result, or completed classroom record.

### 教学环境、练习与评价边界

Resolve delivery details only when they would change the learning result:

- self-study or live facilitation, instructor support, available time, device, and
  classroom or workplace context;
- whether a demonstration, static practice, staged reveal, instructor-led judgment,
  or review is needed;
- expected answer or feedback behavior, including whether an open question has no
  single correct answer; and
- the exact completion, assessment, attendance, certification, and learning-effect
  boundary.

Do not ask for mode, duration, instructor support, practice, or assessment by default.
Use them only when they change progression, examples, practice, or the honest promise.

### 最大缺口规则

After each pass, ask at most the one largest still-missing item whose answer could
change the learning path, key example, practice result, target capability, or hard
knowledge boundary. Reuse the shared 0-6 question budget, repetition rule,
information-gain stop, and hard boundaries; do not add a teaching intake cycle,
course questionnaire, or independent confirmation round.

Route low-risk transitions, illustrative situations, and expression to output-first
production. Never creatively complete a real rule, factual teaching claim,
operational or safety step, quotation, source, real learner result, attendance,
score, certification, or achieved learning effect.

## design-ready 条件

The shared design-ready gate must pass, plus these learning-design decisions must be
sufficiently clear:

- learner group, existing baseline, prerequisite knowledge, application context,
  target capability, and observable performance;
- instructional scope, exclusions, responsibility boundary, and the difference
  between exposure, understanding, explanation, operation, and contextual application
  relevant to this result;
- concept/procedure dependencies, progression logic, terminology, correct examples,
  counterexamples, misconceptions, and failure modes;
- source identity, checked scope, and actual strength for important knowledge, rules,
  facts, procedures, safety, compliance, and other high-risk guidance;
- practice or review need, instructions, expected response, answer/feedback behavior,
  and open-response boundary where applicable;
- self-study/live facilitation, duration, instructor support, and environment only
  where each changes the design; and
- completion, assessment, attendance, certification, learning-effect, unresolved-gap,
  and delivery boundaries.

Design readiness means the artifact can support the declared learning path. It does
not mean a learner has completed or mastered it. When critical knowledge or a safe
procedure lacks adequate support, block that teaching claim or explicitly narrow the
scope; disclosure cannot turn invented knowledge into instruction.

### 设计简报增量

Write these customer-readable fields inside the one existing Report Design Brief's
adaptive `场景特有决策` section. Reuse the current ledger; do not create a second
brief, lesson plan, syllabus, course table, or questionnaire. Do not add a
Profile-specific confirmation round.

- `学习者与已有基础`: learner group, prior knowledge, experience, vocabulary, and
  relevant differences;
- `目标能力/可观察表现`: what the learner should understand, explain, perform, judge,
  or apply and in what context;
- `先备知识与范围边界`: prerequisites, instructional scope, exclusions, and hard
  responsibility or safety limits;
- `学习进阶/概念依赖`: sequence logic, concept/procedure dependencies, and where
  misunderstanding would break later learning;
- `关键示例、误解与失败模式`: sourced or illustrative status of examples,
  counterexamples, misconceptions, and failure modes;
- `练习/回顾与反馈方式`: only when needed, including instructions, response type,
  answer/feedback behavior, and open-question boundary;
- `授课/自学环境及讲师支持`: only conditions that change the artifact, such as
  self-study/live mode, supplied duration, instructor support, device, or context;
- `完成/评价边界`: what participation, completion, assessment, certification, and
  learning effect are and are not established; and
- `关键风险与交付边界`: unsupported knowledge, high-risk guidance, missing examples,
  practice limitations, unresolved items, and the honest delivery promise.

Record reversible inferences and their bases in the existing `待确认项`. Display and
confirm the complete current brief once. Profile selection, complete-brief
confirmation, and current-file Production Authorization remain three independent
facts.

## 叙事任务

### Golden Path

1. **Enter through shared state.** Establish or inherit the material route, task
   intent, use mode, content length, source bindings, and exactly one primary Profile.
   Do not route here from a training label, instructor presence, explanatory content,
   or presentation mode alone, and do not reopen known horizontal values.
2. **Bind learner and observable outcome.** Establish the learner baseline,
   prerequisites, target capability, application context, scope, and exclusions. Ask
   only the current largest result-changing gap when one remains.
3. **Audit knowledge and dependencies.** Verify the concepts, rules, facts,
   procedures, terminology, safety/compliance points, dependencies, misconceptions,
   and failure modes at their required source strength. Never fill a knowledge gap
   merely to make a course look complete.
4. **Derive the learning progression.** Build the sequence from the target outcome,
   often performing the jobs of activating prior knowledge or establishing meaning →
   core concept/method → stepwise demonstration or worked example → learner practice,
   judgment, or review → misconception correction → reusable summary or next step.
   Use only the jobs this learning result needs; do not turn them into fixed chapters.
5. **Align examples, practice, and feedback.** Make each example or counterexample
   serve a target distinction. Ensure practice instructions, learner task, answer or
   feedback, and subsequent explanation agree. Do not assign a unique model answer to
   an open question unless the source and learning design establish one.
6. **Choose only supported learning behavior.** Use static prompts, visible examples,
   instructor-led discussion, or monotonic `fragment-v1` reveals when useful. Keep
   every reading final state complete. Do not implement automatic scoring, learner
   state, completion tracking, certificates, an LMS, or a quiz engine.
7. **Protect the completion boundary.** Label illustrative situations and generated
   practice accurately. Do not state that learners attended, completed, passed,
   mastered, were certified, or achieved an effect without eligible records.
8. **Use the one shared brief and authorization chain.** Add only the fields above to
   the current Report Design Brief, obtain its ordinary complete-brief confirmation,
   then pass current-file Production Authorization. Do not add another confirmation
   or treat Profile selection as production authority.
9. **Produce through the existing chain.** After authorization, follow
   `process-playbook.md`, save the first runnable direct-HTML artifact, apply the
   validated visual route and current Runtime, then run specialized plus shared QA
   and delivery gates.

### 页面任务与学习表达

Give each page one real learning job, such as orienting, activating prior knowledge,
explaining, demonstrating, comparing, practicing, giving feedback, correcting a
misconception, or reviewing. A page may use a different composition when its learning
job differs. These are semantic tasks, not fixed chapters, cards, question types, or
page layouts.

In a confirmed reading mode, every necessary explanation, answer boundary, and final
state must be visible without presentation steps. In a confirmed presentation mode,
staged states may support oral order or learner prediction, but they may not hide
knowledge required to understand the complete artifact.

## 证据规则

- Bind target knowledge, factual rules, operational procedures, terminology, correct
  answers, safety/compliance points, and high-risk guidance to eligible sources or
  explicit confirmation at the strength required by the domain.
- Keep source fact, interpretation, editorial simplification, illustrative situation,
  generated exercise, and pending verification distinct. An accessible or polished
  example does not become a verified real case.
- Never invent knowledge, a source, quotation, customer, learner record, result,
  score, attendance, completion, certification, or learning effect. Do not present a
  fictional classroom or customer situation as achieved evidence.
- A worked example's steps and conclusion must agree. A counterexample must actually
  violate the intended rule. Practice instructions, answer, feedback, explanation,
  and review must not contradict one another.
- For an open question, state the evaluation lens or discussion purpose without
  fabricating one exclusive correct answer. For a closed task, make the answer and
  correction logic accurate and traceable.
- Visual scale, instructor emphasis, staged reveal, or repetition cannot raise
  knowledge or evidence strength. Preserve uncertainties and limitations that affect
  safe application.
- Apply the shared source-role/availability, high-risk verification, output-first,
  and `《待核实内容清单》` rules. Ordinary illustrative learning situations remain
  possible only with the required customer-readable label and delivery disclosure.

## 横向参数默认值

- `input_entry_route`: inherit the established material route
- `use_mode`: `presentation` recommendation only after explicit delegation; otherwise inherit or resolve the existing startup choice
- `visual_binding`: inherit the validated visual route
- `evidence_rigor`: `standard`
- `information_density`: `medium`
- `motion_density`: `moderate` recommendation only; require customer selection or explicit delegation
- `continuation_state`: inherit the Handoff decision

These defaults never override a known, confirmed, inherited, or explicitly delegated
horizontal value. `content_length` remains the shared independent choice. Neither an
instructor nor a course label silently selects presentation mode.

## IR 映射边界

Direct HTML remains the default. Only when the IR engineering route is independently
authorized may this Profile guide existing `narrative_unit`, process, comparison,
claim, evidence, source, page-task, final-state, Projection, and optional Speaker Notes
semantics.

Do not add learner, prerequisite, objective, exercise, answer, assessment, score,
completion, certificate, or LMS fields to the Report IR Schema. Do not create a fixed
JSON course model, question bank, quiz engine, scoring algorithm, Profile-triggered IR
path, Compiler branch, or Validator bypass. The customer-readable learning-design
state belongs in the confirmed Report Design Brief and project-local working record;
any authorized IR remains downstream.

## Runtime/主题使用

Use only the established reading or single-screen presentation mode, validated
built-in/project/enterprise visual route, current page semantics, and current Runtime.
Existing `fragment-v1` may reveal a demonstration, prompt, or feedback monotonically;
the complete final state must contain all content needed to learn or review the page.

The Profile does not add a teaching theme, LMS, quiz engine, automatic scoring,
learner state, completion tracking, certificate generation, dual-screen presenter
view, cross-page morphing, complex state, new interaction, or persistent training
system. Theme and motion cannot establish mastery or learning effect.

## QA 验收

Run all existing objective QA, traceability, asset/browser QA, current-file
authorization rechecks, Runtime/editor checks where applicable, Handoff validation,
and delivery gates. In addition, verify:

- `objective-content-example-practice-review alignment`: every target capability maps
  to sufficient content, the right example or demonstration, any applicable practice
  and feedback, and a usable review without unrelated filler;
- learner baseline, prerequisite order, concept/procedure dependency, terminology,
  step sequence, safety boundary, and high-risk knowledge source remain complete and
  consistent;
- worked examples, counterexamples, failure modes, fictional situations, generated
  practice, and real cases use accurate labels and do not exchange evidence status;
- practice instruction, prompt, expected response, answer, feedback, explanation, and
  later review agree, while open questions are not given a fabricated unique answer;
- reading mode exposes every necessary final state; presentation reveals are
  monotonic and do not hide knowledge needed for independent understanding;
- factual rules, procedures, answers, safety/compliance points, and high-risk guidance
  resolve to their eligible sources and do not exceed checked scope;
- no fictional situation is presented as a real customer/classroom result and no
  learner attendance, completion, score, pass, mastery, certification, or effect is
  claimed without adequate records; and
- the exact current artifact still passes shared technical, browser, asset,
  authorization, Handoff, and delivery checks without claiming unsupported LMS,
  scoring, tracking, or certificate behavior.

Any failure remains a Profile-specific QA failure in addition to the shared gate; it
does not replace or collapse existing QA and delivery conclusions.

## 能力叠加与冲突处理

Research evidence, brand identity, decision explanation, or live delivery may be
bounded overlays with a stated source Profile, reason, and affected scope. They may
not import another Profile's complete intake, design-ready gate, narrative sequence,
artifact set, or QA workflow.

Keep this Profile primary while learning transfer and observable learner capability
remain the dominant product. If audience agreement or purchase becomes dominant,
switch to `live-presentation-persuasion` or
`brand-communication-editorial-publishing`; if the method-and-evidence-backed answer
becomes dominant, switch to `research-analysis-argumentation`. Rebuild only affected
decisions, reuse the existing complete-brief confirmation, and never run two Golden
Paths in full.
