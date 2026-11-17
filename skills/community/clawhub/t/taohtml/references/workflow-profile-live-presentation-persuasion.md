# 现场演讲与说服表达

## 身份与版本

- `profile_id`: `live-presentation-persuasion`
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

Use as primary when the presenter-audience relationship and real-time spoken delivery
are central, and the artifact must move listeners from a current belief or resistance
toward a defined understanding, decision, or action through oral sequence, visible
proof, emphasis, and controlled reveals.

Route by this dominant business outcome. `presentation` use mode, a deck filename, or
a desire for animation is not sufficient by itself.

## 排除范围

Do not use as primary merely because presentation mode is selected. Use another
Profile when the artifact's dominant success condition is independent formal reading,
research validity, recurring management control, or compliance with an authoritative
rule/scoring matrix.

Do not force a sales CTA, offer, price, or conversion page into a non-sales talk. Do
not use this Profile to promise a dual-screen presenter view, embedded speaker-notes
UI, cross-page morphing, complex new animation, a new Runtime state model, or any
feature absent from `runtime-contract.md`.

## 成品

A presentation-ready offline HTML deck within the current Runtime boundary, with:

- a clear audience movement and oral story spine;
- claims and decisive evidence synchronized for live explanation;
- intentional transitions, emphasis, climax, closure, and next step;
- complete readable final state on every staged page;
- optional speaker-support content only when requested and deliverable through an
  existing supported path; and
- specialized presenter-operability QA plus all standard delivery evidence.

The result has no required duration, chapter count, page count, reveal count, poster
style, or roadshow structure.

## 所需信息

Reuse eligible conversation, source, confirmed Material Understanding Summary, and
still-supported handoff state first. Maintain the shared
`known | confirmed | inferred | missing` ledger; do not expose a Profile questionnaire.

### 受众移动状态

Resolve only what materially changes the live result:

- the audience's current understanding, belief, resistance, or competing priority;
- the understanding, decision, or action the talk should create;
- the presenter's relationship, authority, trust, and responsibility boundary with
  that audience;
- which evidence can genuinely change the audience's judgment; and
- any duration, venue, device, projection, connectivity, or interaction constraint
  already supplied.

A duration is optional. Record and honor a hard duration when the user supplies one,
but never ask for it by default or use its absence to block design readiness.

### 最大缺口规则

After each pass, ask at most the one largest still-missing item whose answer could
change the audience movement, central claim, decisive evidence, story spine, final
action, or responsibility boundary. Reuse the shared intake budget, repetition rule,
information-gain stop, and hard boundaries. Route ordinary missing examples,
transitions, or expression to creative supplements rather than extending intake.

## design-ready 条件

The shared design-ready gate must pass, plus these live-delivery decisions must be
sufficiently clear:

- audience current state, target movement, presenter relationship, and main
  resistance;
- central claim, decisive evidence, evidence limitations, and oral story direction;
- the intended closure or next step, with the existing verified real action path only
  when the confirmed objective requires an external action;
- supplied venue/device/duration constraints and any projection-safety boundary; and
- whether speaker-support content is requested and actually supported, without making
  that optional choice a readiness blocker.

### 设计简报增量

Write the following customer-readable fields inside the one existing Report Design
Brief's adaptive `场景特有决策` section. Reuse the current ledger; do not create a
second brief, Profile questionnaire, or Profile-specific confirmation round.

- `受众当前状态`: present understanding, resistance, and competing priority;
- `目标移动`: intended understanding, decision, or action;
- `核心主张`: the main proposition the audience must retain;
- `决定性证据`: evidence expected to change judgment, with strength and limits;
- `主要阻力`: the strongest objection, trust gap, or attention barrier;
- `故事脊柱`: live tension, oral sequence, climax, closure, and transition logic;
- `现场约束`: supplied duration, venue, device, projection, connectivity, and
  interaction conditions; omit unknown optional duration rather than asking for it;
- `动效/口播意图`: page/state focus order, reveal rationale, and requested supported
  speaker assistance; and
- `最终行动`: conclusion, decision, or next step, plus an exact verified action path
  only when external action is part of the goal.

Record reversible inferences and their bases in the existing `待确认项`. Display and
confirm the complete current brief once. Brief confirmation remains distinct from
current-file Production Authorization.

## 叙事任务

### Golden Path

1. **Enter through shared state.** Establish or inherit the material route, task
   intent, use mode, content length, source bindings, and one primary Profile under
   the shared contracts. Do not route here merely because `presentation` is selected
   and do not reopen known decisions.
2. **Define the audience movement.** Make current state, target movement, presenter
   relationship, decisive evidence, and principal resistance explicit. Ask only the
   current largest result-changing gap when one remains; duration is never the
   automatic question.
3. **Build the oral story spine.** Establish a live tension or problem, sequence
   claims and proof in spoken-comprehension order, make decisive evidence visible when
   its claim appears, and create purposeful transitions, emphasis, climax, closure,
   and next step. Do not force sales content into a non-sales talk.
4. **Assign page roles and state intent.** Give every page one semantic job and a
   complete reading final state. Use staged states only when they serve oral order or
   visual focus. Specify what is initially visible, what changes together, which
   object is emphasized, and what the complete final state must contain without
   authoring arbitrary HTML/CSS/JS.
5. **Bound speaker support.** Generate speaker-support content only when the user
   needs it and the current production/delivery path can provide it. Keep it as
   support for the stable page structure; do not promise embedded notes, dual-screen
   UI, or other unimplemented Runtime behavior.
6. **Use the one shared brief and authorization chain.** Add only the fields above to
   the current Report Design Brief, obtain its ordinary complete-brief confirmation,
   then pass current-file Production Authorization. Do not introduce another
   confirmation or treat brief confirmation as formal-production permission.
7. **Produce through the existing chain.** After authorization, follow
   `process-playbook.md`, save the first runnable direct-HTML artifact, apply the
   validated visual route and current Runtime, then run the specialized plus shared
   QA and delivery gates.

### 页面状态与动效意图

Use motion to serve spoken order and focus, not to decorate every page. A page may be
fully static when that is clearer. For a staged page:

- define a monotonic visible sequence whose final state contains every page block;
- group objects that must change together and make the focal object clear at each
  step;
- keep the decisive evidence visible at the moment its claim is explained;
- preserve the distinction between step navigation and whole-page navigation; and
- rely on the existing page, return-state, and page-boundary behavior rather than
  inventing cross-page continuity.

Useful semantic page roles include tension, question, proof, mechanism, contrast,
decision, synthesis, and closure. Visual emphasis may use scale, composition,
contrast, evidence placement, and the existing state sequence. It must not force the
same poster treatment or reveal pattern onto every page.

## 证据规则

- Evidence strength is unchanged by confident delivery, visual scale, animation, or
  a speaker's emphasis. Match the spoken claim to the actual verification status.
- Show decisive evidence with the claim it supports; do not postpone essential proof
  until after the audience has been asked to accept the conclusion.
- Preserve limiting, refuting, and uncertain evidence when it affects the audience's
  judgment. A stage sequence must not temporarily create a stronger unsupported claim.
- Keep illustrative, simulated, projected, disputed, and pending-verification content
  under the existing disclosure and `《待核实内容清单》` rules. Use adjacent labels only
  where the shared contract requires them.
- Never invent a quotation, source, customer outcome, identity, metric, action path,
  or high-risk fact for dramatic effect.

## 横向参数默认值

- `input_entry_route`: inherit the established material route
- `use_mode`: `presentation` recommendation only after explicit delegation; otherwise inherit or resolve the existing startup choice
- `visual_binding`: inherit the validated visual route
- `evidence_rigor`: `standard`
- `information_density`: `medium`
- `motion_density`: `moderate` recommendation only; require customer selection or explicit delegation
- `continuation_state`: inherit the Handoff decision

These defaults never override a known, confirmed, inherited, or explicitly delegated
horizontal value. `content_length` remains the shared independent choice. A
presentation recommendation never substitutes for the existing use-mode decision.

## IR 映射边界

Direct HTML remains the default. Only when the IR engineering route is independently authorized
may this Profile guide an existing `presentation`
Projection, page task and Visual Intent, monotonic State Sequence, and optional
Speaker Notes. Existing `claim`, `evidence`, and `narrative_unit` semantics remain the
only content/evidence model.

Do not add an audience-movement, speaker-support, or animation field to the Report IR Schema.
Do not create a Profile-triggered IR route, arbitrary HTML/CSS/JS,
non-monotonic state graph, Compiler branch, or Runtime promise. Strong models may
propose new page expressions only when they resolve to existing verifiable semantics
and current Runtime capabilities.

## Runtime/主题使用

Use only the established current task mode and validated visual route. In
presentation mode, the existing `fragment-v1` contract may provide progressive
reveal, grouped steps, focus changes expressible through current page state, complete
final-state visibility, whole-page jumps, backward steps, and per-page return-state
preservation.

Follow the current navigation, page boundary, controls, fullscreen, edit-mode, and
viewport contracts exactly. Do not claim cross-page morphing, dual-screen presenter
view, embedded speaker-notes UI, complex animation editing, new input controls, or
unimplemented Runtime states. Theme choice remains independent and may not expand the
Runtime.

## QA 验收

Run all existing objective QA, Runtime/editor checks where applicable, traceability,
asset/browser QA, authorization rechecks, Handoff validation, and delivery gates. In
addition, verify:

- the audience current state, intended movement, presenter relationship, main
  resistance, and final next step are clear;
- the oral sequence earns its conclusion and has usable transitions, emphasis,
  climax, closure, and no gratuitous sales CTA;
- each important claim and its decisive evidence appear in sync, without stagecraft
  upgrading evidence strength or hiding material counterevidence;
- every page has a complete readable final state and any staged sequence is monotonic,
  purposeful, and operable by the same forward action;
- step advance, whole-page navigation, reverse step, page return-state, first-page
  boundary, and final-state-before-leave behavior match the current Runtime;
- controls, page number, hash route, fullscreen, auto-hide, links, inputs, modals, and
  edit-mode event handling are accurate on the exact current artifact;
- the target presentation viewports keep every active page inside the 16:9 canvas,
  preserve safe projected bounds and text readability, and report any required QA
  opt-out; and
- speaker-support content, when supplied, matches the page/state sequence and is not
  represented as an embedded or dual-screen Runtime feature.

Any failure remains a Profile-specific QA failure in addition to the shared gate; it
does not replace or collapse the existing QA and delivery conclusions.

## 能力叠加与冲突处理

Decision comparison, research evidence, teaching explanation, or rule-response
content may be bounded overlays with a stated source Profile, reason, and affected
scope. They may not import another Profile's full intake, design-ready gate, narrative
sequence, artifact set, or QA workflow.

If a formal scoring or eligibility matrix determines success, keep
`rule-response-application-defense` primary and add live-delivery capability only. If
the audience must primarily make or approve a decision from options and the live
delivery is secondary, keep `proposal-planning-decision` primary and use only a
bounded live-delivery overlay.
