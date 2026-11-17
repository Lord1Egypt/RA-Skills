# Intake Workflow

Use this workflow after identifying the available input and before editing or creating HTML. Apply it to every route, with the source gate appropriate to that route. For an existing project, first read `project-handoff.md` and set the independent `new_build | review_only | continue_existing` task-intent overlay. That overlay does not add a fourth content route.

## State Machine

Move through these states in order:

| State | Result | Exit condition |
|---|---|---|
| H0 Task intent | New build, read-only review, or continuation is recorded independently from content route | The user's requested action establishes `new_build`, `review_only`, or `continue_existing` |
| S0 Route handshake | `idea_only`, `word_pdf`, or `existing_ppt_html` is recorded as `route_selected` | A specific topic, an eligible bound source, an explicit route/material intent, or the user's answer to the latest active route options establishes only the route |
| S0B File source acquisition/binding | A file route has one eligible accessible source recorded as `source_bound`; `idea_only` bypasses this state | The current upload, resolvable exact path, task-instruction source, or user-confirmed discovered candidate is bound; otherwise request the source and stop in S0B |
| S0A Startup completion | Reading/presentation and concise/standard/detailed are selected | Choices are known, evident from the input, or explicitly delegated |
| S1 Source grounding | The available idea or source is represented accurately | The route-specific source gate passes |
| S2 Content design completion | Only ordinary outcome-changing decisions and hard-boundary gaps are resolved | The project passes the design-ready gate, or intake stops on a minimum hard boundary |
| S2A Independent design choices | The visual source is resolved; a built-in route has one exact theme; motion density is recorded for every route | Each applicable choice is explicitly user-selected or explicitly delegated to TaoHtml; the ordinary clarification count and no-gain rule cannot skip this gate |
| S3 Reference VI | On the supported static-reference route, one unified VI design standards board is shown; other visual routes bypass this state | The user clearly confirms the exact current board and its conversation reference is recorded, or the state is not applicable |
| S4 Design brief | One customer-readable brief is shown | The user explicitly confirms the current brief |
| S5 Production | HTML, visual system, presentation behavior, and objective QA are completed | Objective failures are fixed |
| S6 Delivery | Files, checks, and a structured verification handoff are reported | Deliverables are usable and creative supplements are easy for the customer to review |

Apply the source gate as follows:

- **Idea only**: seed the ledger from the conversation. Do not create or ask the user to confirm a fictional Material Understanding Summary.
- **Word/PDF**: require `source_bound` in S0B before asking any startup question or reading material; then show the Material Understanding Summary defined in `material-understanding.md` and wait for confirmation or correction.
- **PPT/HTML**: require `source_bound` in S0B before asking any startup question or reading material; then show the same source-grounded Material Understanding Summary, preserve its confirmed core viewpoints, and resolve faithful migration versus reorganization only if both remain reasonable.

`route_selected` and `source_bound` are independent facts. Selecting Word/PDF or
PPT/HTML, including with a compact `2` or `3`, exits S0 but cannot exit S0B. While a
file route remains in S0B, the only user-facing action is to request an upload or a
resolvable exact path and then stop. Do not spend that turn on use mode, length,
audience, Workflow Profile, material understanding, filesystem search, or content
reading.

For `review_only`, stop after the read-only role/availability map in
`project-handoff.md`; do not enter S0-S6 merely to read the handoff. For
`continue_existing`, apply the Continuation Decision Matrix there before S0. A clear
`meaning_preserving_local` revision skips S0-S4 and enters only bounded revision,
applicable current QA in S5, and delivery verification in S6. A `meaning_changing`
revision reuses still-supported interpretations and decisions, then applies only the
affected source gate and delta intake. Do not replay the full intake.

Never write a Report Design Brief while a minimum hard-boundary gap remains. On a new
build or meaning-changing continuation, never write HTML before the current brief is
explicitly confirmed. A meaning-preserving local continuation is the explicit matrix
exception: it does not create or reconfirm a brief and may revise only the exact
delivered artifact inside its semantic boundary. Ordinary absent facts are not a
reason to stop: plan reasonable creative supplements, finish the report, and disclose
the generated details at delivery.
On the static-reference route, never write the brief before the current VI board is confirmed.

For a new build or meaning-changing continuation, maintain the exact current-task
state and allowed actions in `production-authorization.md`. A Material Understanding
Summary, VI standards board, and Report Design Brief are confirmation artifacts.
Formal report HTML, browser QA, and delivery on that path remain forbidden until the
machine gate authorizes them for the current task. A meaning-preserving local
continuation does not fabricate a new authorization state; it preserves the exact
delivered baseline and still runs every applicable current artifact QA and delivery
check. Do not treat a formal or nearly finished HTML deck as a confirmation preview.

## New Invocation Handshake

Every `new_build` or `meaning_changing` continuation that will create or revise HTML
starts at S0 unless the route is already established by the current bound handoff. A
`meaning_preserving_local` continuation does not reopen S0. A `review_only` request
records the route when the available handoff proves it and otherwise leaves it
unresolved without asking the three-route question. Establish only the current task
entry in this first phase.

Treat the current message as route-bearing only when it contains at least one of:

- a specific topic, question, claim, or outcome that the user clearly wants TaoHtml
  to turn into a report; or
- an upload, resolvable exact path, or task-instruction source eligible under `Source
  Binding` below; or
- an explicit file-route selection, filename, unavailable attachment, or material
  description identified as intended input, which may select the route but cannot
  establish `source_bound` by itself.

When any is present, infer the matching route without asking for it again. A
specific topic enters the idea-only startup path. An eligible accessible file source
may establish both the matching route and `source_bound`. A file description,
unresolved filename, unavailable attachment, or route choice without an eligible
source establishes only `route_selected` and enters S0B. For a new build or
continuation, when neither is present, show exactly one route choice with **Idea only
/ Word or PDF: upload the file or provide its complete path / Existing PPT or HTML:
upload the file or provide its complete path**, record that option set as
`latest_options`, and stop. Do not inspect the workspace, read `input/prompt.md`,
summarize materials, draft a brief, or create HTML while S0 is unresolved. A
read-only handoff is the sole exception to the route question, not a fourth route.

Judge semantic binding from the message's task meaning, not from a blacklist or an
enumeration of tokens. Text that merely enables sending, acknowledges the Skill, or
signals attention without identifying a report topic or material supplies no route.
This rule must generalize across languages, punctuation, emoji, and platform UI.

### Conversation-Scoped Option Binding

Maintain at most one active option record:

```text
latest_options = decision id | Agent turn | exact choices | active/inactive
```

A short label, ordinal, or compact answer binds only when it is a plausible direct
answer to the Agent's most recent active option record in this same conversation.
Consume the record after one answer and invalidate it whenever a newer option set or
changed task supersedes it. Never map a compact answer to section numbering in this
Skill, an earlier conversation, a platform menu, or a route number remembered from
documentation. Thus a compact answer after the Agent has just shown the three entry
routes can select that route; the same compact text attached to a fresh invocation
cannot.

## File Source Acquisition And Binding

Apply this low-freedom gate immediately after S0 for `word_pdf` and
`existing_ppt_html`. Do not apply it to `idea_only`. If the exact source is already
eligible and accessible, bind it once and continue without requesting it again. If
an explicit path cannot be resolved or accessed, report that exact-path problem and
request a corrected path or upload; do not search its parent, siblings, the current
working directory, or the wider workspace.

Candidate discovery is disabled by default. It becomes available only when the user
explicitly asks TaoHtml to find the source and identifies, or has already clearly
placed in scope, a narrow directory. Discovery may inspect metadata needed to present
exact candidate paths, but it must not open, extract, parse, summarize, or otherwise
read candidate content. Show the exact path or paths and stop for confirmation. Only
the confirmed candidate becomes `source_bound`; do not auto-bind even a single match.

### Source Acquisition Decision Table

| Case | route | source_status | discovery_authorization | allowed_actions | next_state | forbidden_actions |
|---|---|---|---|---|---|---|
| `idea_only_topic` | `idea_only` | `not_applicable` | `not_required` | `continue_startup` | `S0A` | `request_source,filesystem_search,source_read` |
| `word_pdf_missing` | `word_pdf` | `missing` | `absent` | `request_source,stop` | `S0B` | `use_mode_question,length_question,audience_question,filesystem_search,candidate_discovery,source_read` |
| `existing_ppt_html_missing` | `existing_ppt_html` | `missing` | `absent` | `request_source,stop` | `S0B` | `use_mode_question,length_question,audience_question,filesystem_search,candidate_discovery,source_read` |
| `current_upload` | `file_route` | `accessible_current_upload` | `not_required` | `bind_exact_source,continue` | `S0A` | `request_source,candidate_discovery,broad_search` |
| `explicit_path` | `file_route` | `resolvable_exact_path` | `not_required` | `bind_exact_path,continue` | `S0A` | `request_source,parent_search,sibling_search,broad_search` |
| `task_instruction_source` | `file_route` | `accessible_task_bound_source` | `not_required` | `bind_exact_source,continue` | `S0A` | `request_source,candidate_discovery,broad_search` |
| `authorized_directory_discovery` | `file_route` | `missing` | `explicit_narrow_directory` | `metadata_discovery,show_exact_paths,stop` | `S0B` | `content_read,extract,summarize,auto_bind,startup_questions` |
| `confirmed_candidate` | `file_route` | `confirmed_candidate` | `explicit_narrow_directory` | `bind_confirmed_candidate,continue` | `S0A` | `read_unconfirmed_candidate,broaden_search` |
| `workspace_or_history_residue` | `file_route` | `unbound_workspace_file` | `absent` | `request_source,stop` | `S0B` | `auto_bind,filesystem_search,candidate_discovery,source_read` |

## Source Binding

Maintain a source ledger separate from the design and creative-supplement ledgers.
A local or uploaded material is eligible only through one of these bindings:

1. `current_upload_or_user_explicit`: the user uploads it now and it is available in
   this session, or provides one resolvable exact file path for this task;
2. `task_instruction_explicit`: the current task instruction explicitly declares one
   accessible file or prepared input as this run's source; or
3. `candidate_confirmed`: after the user explicitly asks TaoHtml to find the source
   in a narrow in-scope directory, the Agent presents an exact metadata-only
   candidate path and receives confirmation to use it.

An external network or connector source retrieved by the Agent uses
`agent_retrieved_external` only when the current task authorizes browsing/evidence
retrieval and the Agent records the exact URL or stable locator, retrieval time,
inspection coverage, supported claim, and verification result. This is not a fourth
local-file binding: never apply it to a workspace candidate or use it to broaden
filesystem discovery.

Mere workspace presence, the current working directory, a conventional filename such
as `input/prompt.md`, a directory convention, or residue from a previous task is never
a binding. Do not silently promote such a file to `known`, even when its content looks
relevant. Before route establishment, do not scan for candidates at all. Route
establishment alone still does not authorize discovery: a compact `2` or `3` is only
a route selection. Without the user's explicit request to find a source, request an
upload or resolvable exact path and stop.

A read-only handoff whose content route remains unresolved may inspect only the
task-scoped attachment explicitly bound for the handoff audit, as defined in
`project-handoff.md`. It may inspect directory metadata to present an exact candidate
only after the user explicitly asks it to find that source; it still may not read
candidate content or broaden the search.

When explicitly authorized, candidate discovery must stay inside the narrow directory
the user specified or clearly placed in scope and remain metadata-only. Do not
recursively scan a home directory, Desktop, Downloads, platform cache, cloud-sync
root, unrelated workspace, or other broad user location. A shell command that finds
no match in one checked location is not evidence that the item was cleaned, deleted,
or permanently lost. Apply the availability states in `project-handoff.md`; keep it
`not_yet_verified` or `handoff_record_only` unless the user or an authoritative
platform/source state confirms the exact item is missing.

For every material actually used, record:

```text
source identity/path | source_binding | source role | availability status |
evidence verification | inspection coverage | binding reason |
bound conversation/task turn
```

Carry these fields into the Material Understanding Summary and the Report Design
Brief's source records. A customer-bound or independently verified source remains a
real source and must never be relabeled as a creative supplement.

For handoff work, use the seven source roles, six availability states, and independent
evidence-verification field defined in `project-handoff.md`. A secondary handoff
summary can establish what was previously reported, and a current artifact can
establish what is presently rendered; neither establishes the provenance of
underlying claims without the original source or an explicit confirmation permitted
by that reference. A retrieved third-party/public source uses
`external_public_evidence | external_retrieved_inspected`; never relabel it as
customer material or Agent-generated content.

## Decision Ledger

Maintain these buckets internally; do not expose them as a questionnaire:

```text
known | confirmed | inferred | missing
```

- **known**: stated in the current conversation or directly supported by the source.
- **confirmed**: explicitly accepted or corrected by the user.
- **inferred**: a reversible ordinary design decision TaoHtml can make from context or user delegation; record its basis and expose it in the brief. A built-in theme or motion density enters this bucket only after explicit delegation, never from context alone.
- **missing**: an outcome-changing decision or hard-boundary fact that is not yet known and cannot be safely delegated.

Rebuild the ledger after reading each source and update it after every answer. Move information instead of copying it across buckets. Treat a stated route, use mode, audience, desired outcome, content length, real action path, or hard presentation duration as `known`; do not ask for or confirm the same information again. Do not ask about any other `known`, `confirmed`, or safely `inferred` item.

For `continue_existing`, seed the ledger from still-readable verified artifacts and
the handoff role/availability map. Preserve a distinction between inherited verified
facts, secondary claims, and currently unavailable material. Ask only about a delta
that can change the requested result; do not turn takeover into a fresh interview.
When the requested delta is clearly `meaning_preserving_local`, do not rebuild this
ledger as a new intake; retain it only as the semantic baseline for post-change
traceability.

The design ledger is not the delivery verification list. During production, maintain a separate creative-supplement ledger with `page/content | supplement type | source status | suggested action`. A missing ordinary scene, number, viewpoint, or expression may enter this ledger directly instead of becoming another intake question. Customer-provided and independently verified facts stay in `known` or `confirmed`; never relabel them as creative supplements.

## Desired Action And Real Action Path

Keep two decisions separate:

- **Desired action**: what the audience should decide or do after the report.
- **Real action path**: the exact channel through which the audience can complete that action, such as a verified URL, host-agent invocation, installation command, booking route, download location, or contact detail.

Treat trial, purchase, booking, download, installation, contact, registration, subscription, and similar external-action goals as **conversion objectives**. A conversion objective is not design-ready until the desired action and a real action path are both resolved. Do not ask for an action path when the report is explanatory, educational, or internal and its confirmed goal does not require an external action.

Accept an action path only when it is:

1. explicitly provided by the user;
2. present in the source material or project context and verified against that context; or
3. selected under explicit user delegation and independently verified by the Agent before the brief.

Do not ask for an action path already supported by the source or project context; record the value, source, and verification result in the ledger instead. Where independent verification is required, establish that the intended audience can use the complete channel and that it leads to the intended action. For URLs, open the target and confirm its purpose. For host-agent syntax or commands, check authoritative host or project documentation without triggering the external action. For user-provided contact details or prices, preserve the exact value and mark it as user-provided rather than implying independent verification. A QR code is a presentation of a verified value, not a source: decode it and compare the result with that value before delivery.

Never invent a URL, QR code, contact detail, price, command, or product entry. If the user delegates channel selection but the Agent cannot verify a candidate, keep the action path in `missing`.

When a conversion objective lacks a real action path, ask one minimal decision question at the point where it is the largest outcome-changing gap: request the exact channel, request authorization to locate and verify one, or offer to explicitly downgrade the goal so the report no longer promises direct action. This prompt counts toward the same six-question limit; it is not a fixed questionnaire item. A downgrade is valid only when the user clearly accepts the changed goal.

## Startup Decisions

Preserve the three product choices:

- **Route**: idea only, Word/PDF, or existing PPT/HTML.
- **Use mode**: reading, where each page stands alone and content is visible by default; or presentation, where tighter copy follows a spoken staged sequence.
- **Length**: concise, standard, or detailed.

Resolve at most one missing startup choice per round and skip every choice already made. Complete the route handshake and, for a file route, S0B source binding before asking use mode or length. If presentation mode is already known, do not ask the user to select the use mode again. Do not bundle route, use mode, and length into one prompt. For a message with a specific idea-only topic, the route is already known and S0B is not applicable. When route and use mode are known but content length is missing, ask one question that offers **concise / standard / detailed**; do not infer a default length without explicit delegation, and do not replace these choices with duration or page-count options.

Estimate the page count dynamically from the actual material after the content length is selected, and record that estimate in the design brief. Never assign or present a fixed page range by length label alone.

Presentation duration is an optional delivery constraint, not a startup choice or a design-ready prerequisite. In presentation mode, do not ask for a duration by default and do not block progress when no duration was given. If the user provides a hard duration, record it as `known`, use it to constrain scope, pacing, and content density, and do not ask the user to repeat or confirm that duration. A hard duration does not replace the content-length choice.

## Idea-Only Judgment Layer

For an idea-only route, evaluate these layers in order and skip any layer already resolved or safely inferable:

1. **Audience and desired outcome**: who should understand, believe, decide, or do what after the report.
2. **Core viewpoint or core question**: the claim the report should establish, or the question it must answer.
3. **Evidence or conclusion-level conflict**: proof required for important claims and any ambiguity that could reverse the main conclusion.
4. **Structure choice**: ask only when multiple chapter structures are genuinely reasonable and would produce meaningfully different reports.

Treat this as a judgment layer, not a four-question form. Minor chapter naming and ordinary delivery defaults may be low-risk inferences. Built-in theme and motion density are handled only by the independent design-choice gate below.

## Visual Source Selection

Resolve the visual source only after content and chapter structure are clear enough to judge fit.

- Read `profile-memory.md` and parse enterprise identity from the eligible current material and conversation before asking for a new visual source. Pass only explicit identity candidates to `profile_store.py resolve`; do not add a fixed identity/reuse questionnaire and do not treat the previous task's choice as a permanent preference. One unique active profile binds automatically without reopening reference images, regenerating VI, or asking whether to reuse. Show its concise customer notice, then continue to the Report Design Brief unless the customer objects. Several candidates, unclear identity, alias conflict, or a current requirement/profile conflict permits exactly one selection question; never guess or combine profiles. A different company/customer always uses a separate profile.
- Interpret “这次不用 / 这次换一个” as a task-local `temporary_override` binding that leaves the active version unchanged. Interpret “以后改用 / 更新公司模板” as a new corporate-fidelity VI confirmation plus immutable profile version and atomic active-pointer switch. Do not perform or imply destructive deletion; use archive when the customer wants the profile out of automatic resolution.
- Reading versus presentation is the current task Runtime mode, not a profile conflict. Run the minimal `profile-reuse` preflight, bind the active corporate version with the current mode, and pass that mode to the renderer. Do not ask the customer to rebuild VI, create v2, or abandon the profile for a mode-only change.
- On every route without a unique active Profile binding, resolve reference availability before presenting a fallback template. Unless a supported reference is already supplied, the customer has already named a concrete built-in system, or the customer explicitly delegates the built-in choice, ask exactly: **本次是否有希望参考的模板、企业母版或喜欢的意向图？有的话请上传静态截图；没有则从内置视觉系统中选择。** This is one independent visual-source decision, not an ordinary clarification question and not an open-ended taste question. A clear “有” starts the reference route and a clear “没有” starts the built-in route; do not combine this question with theme or motion selection. A customer who asks to replace a reused Profile enters this same reference-first choice.
- If the customer provides or confirms a reference, resolve `reference_mode` once. `reconstruct` accepts exactly one static PNG/JPEG/WebP; `corporate_fidelity` accepts one to three representative static PNG/JPEG/WebP screenshots from the same template family. When the user already asks for “企业模板保真”, “公司模板原样采用”, or equivalent screenshot-visible fidelity, record `corporate_fidelity` without asking again. When intent is still unclear, ask one binary question: **参考风格重构**—提取设计语言，允许重新构图和创新；or **企业模板保真**—锁定截图中可见的企业固定元素，只设计各页面壳的安全内容区. Record `reconstruct` or `corporate_fidelity`, count this as one ordinary clarification question, and never repeat it after the answer is known.
- For either mode, read `static-reference-vi.md`. Use the current session for only the minimal readability check defined there. When readable, analyze static visual facts, render one VI board through the shared contract, and wait for clear confirmation of that exact board without requiring a fixed reply phrase. In corporate fidelity, automatically identify each source role unless truly ambiguous; the board must expose all source thumbnails and role bindings, screenshot-visible fidelity boundary, shell-specific locked/editable regions, exact observed/extension/unknown labels, proposed unseen roles, and limitations. Customer corrections before confirmation replace the current contract. Do not require an internal-theme choice, infer dynamic behavior, or begin project-theme generation/report production before confirmation.
- If the user has a clear reference but it is a PPT, webpage, video, state sequence, more than three corporate screenshots, or multiple screenshots for reconstruct, stop at the unsupported boundary and ask for a supported representative raster input. This is not the no-reference route: do not infer movement and do not recommend the eight built-in systems unless the user explicitly abandons the reference route.
- Treat model choice as a platform/session-entry decision. WorkBuddy first use gets one recommendation to use Auto; Codex and Claude Code continue with the current session model. Never ask the user to select or repeatedly switch models inside the intake. If the current session cannot locate reliable static facts, say “当前会话无法可靠读取参考图” and offer only a manual model change followed by a restarted task, or a downgrade to the eight built-in systems.
- Only when no enterprise profile applies, the customer has explicitly declined a reference (or has already named/delegated a concrete built-in system), and no clear reference route is active, read `visual-systems.md`. If the user already specified one concrete built-in system, adopt it directly without displaying the catalog and record the exact decision reference. Show a category subset only when the user has proactively and explicitly constrained the acceptable range of the built-in catalog and that constraint maps unambiguously to one declared category; never infer a catalog-range constraint from project context. Otherwise, in the same round, show every system in the complete current built-in catalog with its exact customer-facing name, one-line description, and bundled preview. Do not hide any entry because the Agent considers it less suitable. Report goal, audience, content, report type, and reading or presentation mode are recommendation inputs only: use them to mark one or two displayed systems as **更推荐**, but never to shrink the catalog; recommendation never replaces complete catalog display. If a user preference or constraint does not map unambiguously to a declared category, show the complete current catalog, reflect that preference in the recommendation reason, and never invent an ad hoc subset. Ask the user to choose once, or invite explicit delegation to TaoHtml; without either, stop at this gate.
- Do not ask open-ended aesthetic questions such as “What style do you like?”. Do not repeat a theme-selection question after the user chooses or delegates.
- The one-time ambiguous reference-mode resolution remains an ordinary clarification and uses the existing counter. The exact built-in theme and motion-density choice are separate design decisions outside that counter. Reaching the six-question maximum or the three-no-gain stop ends ordinary clarification but never selects either value. Do not ask the reference-mode question after explicit intent, and never infer corporate fidelity from an ambiguous request because it creates a fixed-asset lock.
- For every visual route, present `minimal | moderate | rich` as **少量 / 适中 / 丰富**, recommend at most one, and wait for the user's choice or explicit delegation. A Workflow Profile default, static input, project context, question cap, or model judgment is recommendation evidence only. Do not repeat a known motion choice.
- A selected theme fixes a reusable visual grammar, not a palette. Preserve its composition, hierarchy, image treatment, module language, chart/evidence treatment, and motion grammar unless the brief records a necessary deviation.

## Select The Next Question

Before asking, re-read the conversation, available source, ledger, prior attempts, and counters. Then:

1. Remove gaps whose answers are already present or can be safely inferred.
2. Resolve S0 first, then S0B for a file route, then any missing startup choice according to `Startup Decisions`; after startup, rank the remaining gaps by how much they could change narrative, scope, conclusion, evidence, structure, or delivery.
3. Ask only the largest current gap whose answer would change the report design.

For continuation, classify the delta before ranking gaps. A clear
`meaning_preserving_local` revision asks no intake question and does not reopen a
Material Understanding Summary or Report Design Brief. If the class is ambiguous,
ask only the single largest scope-boundary question. A `meaning_changing` revision
removes every unchanged inherited decision, then asks only its largest remaining
gap. Apply the recovery/explicit-confirmation boundary in `project-handoff.md` when
the revision changes real data, provenance, evidence relationships, identity,
achieved outcomes, a core conclusion, structure, scope promise, or responsibility
boundary.

Ask exactly one decision question per round. Do not pack independent questionnaire fields together. Offer 2-3 options only when they are real alternatives and state their design impact briefly.

Treat "decide for me", "not important", or equivalent wording as delegation: choose a reasonable low-risk default, move it to `inferred`, and do not ask again.

For a missing conversion action path, delegation authorizes TaoHtml to locate and verify a channel; it does not authorize invention or an unverified default.

## Question Budget And Stop Rules

Count agent-initiated clarification prompts within the current intake cycle. Count each single-decision startup prompt and the one-time ambiguous reference-mode choice as one. Built-in theme selection, motion-density selection, and confirmation of the displayed Report Design Brief are separate gates and do not count toward this budget.

A read-only handoff uses zero clarification questions and does not start an intake
cycle. A clear meaning-preserving local continuation also uses zero intake questions.
A meaning-changing continuation delta uses this same budget and stop policy; it does
not receive extra questions for previously answered startup or design decisions.

- Allow **0 clarification questions** when the input already passes the source and design-ready gates.
- Treat **3-5 clarification questions** as the ordinary target, not a quota.
- Enforce **6 clarification questions** as a hard maximum, including for the most complex idea-only intake. Do not ask a seventh.
- Ask about the same key gap at most **twice**. On the second attempt, replace the abstract wording with a concrete example or 2-3 real options. After that, infer or block according to risk.
- Track whether each response produces actionable new information: it resolves or narrows a missing decision, corrects the ledger, supplies evidence, or clearly delegates a decision.
- Stop ordinary clarification immediately after **three consecutive rounds without actionable new information**. Then infer all remaining ordinary low-risk gaps and either enter the independent design-choice gate or use the blocked-intake output. Do not infer a built-in theme or motion density.

Stop ordinary clarification immediately when the design-ready gate passes; never continue asking to approach a target or maximum. At the hard maximum, infer reversible ordinary design decisions, route ordinary missing content to the creative-supplement ledger, and stop ordinary clarification. Continue to the independent design-choice gate when no minimum hard boundary remains. Never use budget pressure as permission to cross a minimum hard boundary or select a theme/motion value.

If the user initiates a change to the core goal or scope, invalidate any affected brief and start a new intake cycle with fresh counters. Preserve reusable facts in the ledger, but do not count the first question of the new cycle as question seven of the old one. Local wording, color, layout, or motion revisions do not start a new cycle unless they change the report's meaning or scope.

## Output-First And Hard-Boundary Rules

Infer an outcome-changing ordinary design decision only when a reasonable choice is reversible during brief confirmation and cannot materially change the report's promise, scope, central meaning, factual integrity, or main conclusion. Record the inference and its basis in `待确认项`. Built-in theme and motion density require explicit selection or delegation instead.

Ordinary information gaps do not automatically create a block. TaoHtml may add plausible scenes, numbers, viewpoints, comparisons, examples, and expression as creative supplements when they help complete a useful report. These are pending-verification generated content, not source facts and not automatic errors. Track the exact additions for the delivery list. Put an adjacent `示意 / 模拟 / 待核实` label in the HTML only when a simulated chart, fictional customer case, generated evidence-like artifact, or numeric display could reasonably be mistaken for real proof; keep ordinary projections in the delivery note so risk disclosure does not damage the presentation.

The minimum hard boundaries are:

- never invent a real customer or company identity, quotation, citation, literature, or source;
- never state that an illustrative or fictional case is an achieved customer result;
- explicitly verify legal, medical, financial, safety, and similar high-risk facts before presenting them as guidance or fact;
- never replace, reinterpret as generated, or silently alter a confirmed real source, data point, quotation, or action channel;
- never claim that an audience can complete a conversion action without a verified real action path; and
- never silently choose between goals, conclusions, or structures that materially change the promised outcome or responsibility boundary.

When a conversion objective's real action path remains missing at a stop condition, do not generate a Report Design Brief or begin production. Use the blocked-intake output below, unless the user has explicitly downgraded the goal to one that does not require direct action. Never replace the missing channel with a slogan, a generic process such as “choose material → hand it over → see the result,” or an implied future entry point.

When a minimum hard-boundary gap remains after its second attempt, the six-question maximum, or the three-no-gain stop, do not generate a Report Design Brief and do not begin production. Ordinary missing support belongs in the creative-supplement ledger and must not trigger this block. Output only:

```markdown
# 问诊暂停

## 当前已知
- ...

## 未决缺口
- ...

## 为什么不能推断
- ...

## 最小补充材料
- ...

## 恢复条件
- ...
```

Ask for the smallest specific item that would unlock the decision. Resume the same intake cycle when that item arrives, unless the user changes the core goal or scope.

## Design-Ready Gate

Treat a new build or meaning-changing continuation as design-ready when:

- The audience outcome is clear enough to choose a narrative.
- The core viewpoint or core question and scope are clear.
- Evidence required by the report type is present, explicitly bounded, or separated from planned creative supplements without presenting those supplements as verified proof.
- No unresolved conflict can reverse the main conclusion.
- One chapter structure is selected or only one reasonable structure follows from the ledger.
- Route and use mode are known or evident from the input, length is known or explicitly delegated, and required material delivery constraints are known or safely inferred; optional presentation duration may remain unspecified.
- A Word/PDF or existing PPT/HTML route is `source_bound` before any source grounding or later startup/design work; `idea_only` remains unaffected.
- Every material in use has an eligible `source_binding` and recorded binding reason; no workspace convention or residue is acting as an implicit source.
- For handoff or meaning-changing continuation work, every bound item also has an explicit source role, availability status, evidence-verification status, inspection coverage, support scope, and limitation; secondary summaries and current artifacts are not treated as original evidence, while retrieved public/third-party evidence has its own external role and availability.
- For a conversion objective, the exact real action path, its source, and its verification status are recorded; non-conversion reports do not need this field.
- No minimum hard-boundary item remains in `missing`; ordinary creative supplements may remain pending customer verification.

Stop ordinary clarification as soon as these conditions are met. A clear idea can therefore proceed directly to the independent design-choice gate with zero clarification questions.

## Independent Design-Choice Gate

Apply this gate only after the content and chapter structure are clear enough to make a useful recommendation. It does not add ordinary clarification budget and cannot be skipped by the six-question maximum or the three-no-gain rule.

- Resolve the visual source as one built-in system, a supported static reference, or a validated enterprise Profile binding. Static-reference and Profile routes keep their existing VI/binding gates and set built-in theme selection to `not_required`; never ask them to choose an internal theme as well.
- On the built-in route, a concrete theme already named by the user records `user_selected`, exact `theme_id`, and `decision_ref`. Otherwise display the applicable catalog under `visual-systems.md` and wait. Only an explicit “TaoHtml 决定 / 帮我选” or equivalent records `delegated_to_taohtml` and permits the deterministic lowest-risk choice described there.
- On every visual route, record motion density as `minimal | moderate | rich`, show **少量 / 适中 / 丰富**, and wait for `user_selected` or explicit `delegated_to_taohtml`. TaoHtml may recommend one; it may choose only after delegation.
- On the static-reference route, explicitly confirm the current VI board and record its contract/output paths; earlier agreement to use the reference is not VI approval. On the Profile route, validate the current task binding against the active profile/version and existing project-theme loader. Neither substitutes for the Report Design Brief confirmation.
- Do not ask again after either choice is recorded. If one is known and the other remains pending, ask only for the pending choice.

Do not create or confirm a Report Design Brief until this gate and every route-specific VI/profile/theme gate are complete. Copy both decisions, their selection status, exact decision reference, recommendation basis, and any deviation into the current brief.

## Confirmation Rules

### Material summary gate

For any bound Word/PDF/PPT/HTML material route, ask the user to confirm or correct the displayed Material Understanding Summary. If they correct it, issue an updated summary before continuing. Do not impose this gate on an idea-only input.

### Static-reference VI gate

After the content and structure are clear enough to interpret visual fit, follow `static-reference-vi.md`, show the rendered VI PNG, and ask the user to confirm or correct the current board. Bind any clear confirmation to the exact current artifact and conversation turn; never use a fixed authorization phrase as a cross-task token. If the user corrects any visual item or boundary status, rerender the complete board and request confirmation again.

VI confirmation authorizes only the confirmed-VI handoff to the separate project-theme step. It does not confirm the Report Design Brief and does not authorize formal report production. If the project-specific theme output is not yet available, stop at the handoff boundary rather than substituting a built-in theme.

### Design brief gate

Show one current Report Design Brief and ask the user to confirm or correct that exact artifact. Only a reply that clearly confirms this displayed brief opens production; record its current conversation reference rather than matching a fixed reply phrase. Earlier approval to discuss, use TaoHtml, or begin intake does not count. Brief confirmation is authorization, not clarification, so it remains required even when the clarification counter is already six.

If the user adds source material or changes a core viewpoint after confirmation, invalidate the brief, update it, and ask for confirmation again. During production, resolve non-core omissions with a reasonable default or creative supplement, add the exact item to the delivery verification ledger, and continue instead of repeatedly interrupting the user.

For a meaning-preserving local continuation, do not rebuild the source interpretation
or Report Design Brief and do not request brief reconfirmation. Preserve the exact
delivered baseline and run applicable current QA and delivery validation after the
bounded change. For a meaning-changing continuation, rebuild only the affected source
interpretation and brief fields, then display the complete current brief and use the
existing brief-confirmation gate. Do not restart clarification about unchanged
inherited sections. Previous handoff claims do not open the formal HTML gate.
