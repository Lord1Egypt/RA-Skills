
# TaoHtml

Turn source material or an incomplete idea into a finished HTML report that can be read or presented without further layout work. Optimize for a usable report first: ordinary missing details may be completed creatively, then disclosed for customer verification at delivery.

Treat TaoHtml as two cooperating layers:

- The skill directs material understanding, decisions, visual composition, generation, QA, and delivery.
- The bundled runtime supplies stable navigation, reveal state, reading/presentation modes, and other implemented behaviors.

Do not claim runtime features that are not present in `references/runtime-contract.md`.

## Explicit Invocation

Prefer explicit invocation. Use the host agent's real skill syntax, such as `$taohtml` in Codex. Do not assume `/TaoHtml` is portable across agents.

## Entry Routes

Start every new build or meaning-changing continuation that will create or revise
HTML with a route handshake. A clear meaning-preserving local continuation applies
the handoff overlay first and bypasses this handshake; it starts from the exact
delivered artifact rather than reopening the content route. The current message may
establish the route when it contains a specific report topic, an explicit route
selection, or a source that is explicitly bound to this task. A file-route selection
without an eligible source establishes only `route_selected`. Low-information text attached only so a platform can
send the Skill does not establish a route. Do not classify it with a list of forbidden
words, and do not scan the workspace for a presumed input. A read-only handoff review
applies the overlay below, records the route only when the bound evidence establishes
it, and does not ask an entry-route question.

If the current message already provides a specific topic, explicitly selects a route,
or binds a source, record the matching route and apply its next gate without asking
for the route again. Otherwise show exactly these three entry routes and stop after
this one question:

1. **Idea only**: build the report definition from the conversation, then produce a brief only when it is design-ready.
2. **Word / PDF**: upload the source or provide its complete resolvable path. TaoHtml does not search the local machine or begin material understanding before receiving it.
3. **Existing PPT / HTML**: upload the source or provide its complete resolvable path. TaoHtml does not search the local machine or inspect the existing work before receiving it.

For routes 2 and 3, `route_selected` never implies `source_bound`. If no eligible,
accessible source is currently bound, ask only for an upload or a resolvable exact
file path, then stop. Do not ask about use mode, length, audience, or any later
decision; do not search for or read a file. Continue only after binding the source.
Candidate discovery requires the user's explicit request to find a file and follows
the narrow metadata-only confirmation boundary in `references/intake-workflow.md`.

A short answer or ordinal selects an option only when it answers the Agent's most
recent still-active option set in this conversation. The numbering above is
documentation, not a global command interface. Before the route is established, do
not inspect materials, produce a Material Understanding Summary, create a Report
Design Brief, or write HTML. Read `references/intake-workflow.md` for the option-state
and source-binding rules. Never ask for information already present in the conversation
or an eligible bound source.

## Workflow Profile Routing

TaoHtml is one installed Skill. Its nine business-production paths are on-demand
Workflow Profiles, not separate Skills, input routes, Runtime modes, or Report IR
choices. After the material entry is established, read
`references/workflow-profile-contract.md` and resolve exactly one primary Profile from
the user's explicit business objective plus the semantics of eligible inspected
material. If one path is clear, select it automatically, record the basis, and do not
ask a Profile question or read/display the catalog. Use the contract's Definition
Routing table to read only the selected `definition_ref`; do not load any other
Profile definition.

When the selected definition declares a detailed/implemented Golden Path, execute
that Profile-local sequence and its acceptance additions after loading that one
definition. It refines the shared intake, brief, production, and QA flow; it never
loads another Profile, creates a separate confirmation, or replaces a shared gate.

Only when the primary outcome remains genuinely ambiguous after using the available
semantic evidence, read `references/workflow-profiles.md`, display all nine exact
customer-facing names and primary goals in one round, and ask one question about the
finished report's primary business goal. After the answer, read only that catalog
row's `definition_ref`; do not load the other eight definitions. Do not route with a
keyword blacklist, hard-coded numbers, filename-only matching, or a fixed report-type
mapping. Do not repeat a known goal or ask the user to choose Profile ids, IR fields,
Compiler modes, Runtime features, or theme implementations. Keep input entry,
reading/presentation mode, visual binding, evidence rigor, information/motion density,
and continuation state as independent horizontal parameters. Run only one complete
primary Profile; borrow other Profile capabilities only as bounded overlays. A Profile
default never replaces the existing use-mode or content-length choice unless the user
explicitly delegates that decision under `references/intake-workflow.md`.

## Project Handoff Overlay

Read `references/project-handoff.md` whenever the request concerns an existing
project, handoff record, current artifact, review, or continuation. Record
`new_build | review_only | continue_existing` as a task-intent overlay; this does not
add a fourth content entry. A read-only handoff defaults to zero clarification
questions, does not restart intake, and must not create HTML. Continuing work reuses
still-supported state, first classifies whether the delta preserves meaning, asks
only the largest result-changing gap when one exists, and protects the source/evidence
boundary defined in that reference. For a cross-Agent export, import, or readiness
check, also read `references/project-handoff-schema.md`, use its strict JSON schema,
and run `scripts/validate_project_handoff.py`; never collapse its four independent
results into one PASS.

## Visual-Source Priority

This ordering governs step 5 below. A unique active enterprise Profile remains a known, previously confirmed visual binding and may be reused with its existing concise notice. For every other route, resolve whether the customer has a specific template, enterprise master, or preferred reference image before presenting any fallback theme. Unless a supported reference is already supplied, a concrete built-in system is already named, or the customer explicitly delegates the built-in choice, ask exactly:

> 本次是否有希望参考的模板、企业母版或喜欢的意向图？有的话请上传静态截图；没有则从内置视觉系统中选择。

A clear “有” enters the supported static-reference route and must produce the existing VI design standards board before project-theme compilation. A clear “没有” enters `references/visual-systems.md`, where TaoHtml displays the complete applicable built-in catalog; it must not recommend, display, or select a fallback theme before the reference decision is known. This visual-source decision is independent from ordinary clarification and must not be bundled with theme or motion selection. A request to replace a reused enterprise Profile also enters this reference-first choice.

## Required State Flow

Follow the branch selected by the handoff decision before applying this sequence.
Steps 2-8 are the new-build or meaning-changing production path; a clear
`meaning_preserving_local` continuation goes from step 1 to its bounded revision under
the Runtime boundary in step 9 and the exact-artifact QA/delivery work in step 10. It
does not enter steps 2-8 or manufacture their confirmation artifacts.

1. Read `references/project-handoff.md` when applicable and establish the task intent. For `review_only`, inspect only eligible bound items, report their roles, availability and limits, then stop without a route interview, brief, formal production, or HTML. For `continue_existing`, apply its Continuation Decision Matrix first. A clear `meaning_preserving_local` revision does not enter startup, intake, material-summary, or design-brief gates; preserve the exact delivered baseline and proceed only through the bounded revision plus applicable current QA/delivery checks. Otherwise establish or inherit the content route. On Word/PDF or existing PPT/HTML routes, pass the source-acquisition/binding gate before identifying use mode, content length, or any other startup decision; when the source is unbound, request only an upload or resolvable exact path and stop. After the gate, identify use mode and content length one decision at a time and skip every known choice. For presentation mode, treat a user-provided hard duration as a constraint, but never require duration to start. Record every used material's `source_binding`, role, availability status, evidence verification, inspection coverage, and binding reason; mere workspace presence never qualifies.
2. Read `references/environment-preflight.md` and run the smallest required profile before gated work. For a bound Word/PDF/PPT/HTML source, read `references/material-understanding.md`; run the `pdf` profile before opening or extracting a PDF, then inspect only eligible bound sources, show a Material Understanding Summary with source bindings and source-role/availability distinctions, and wait for confirmation or correction. For an idea-only input, do not invent a source-summary gate. For a `meaning_changing` continuation, summarize only the affected source delta and inherited limits; never promote a secondary handoff summary or current artifact to original evidence. Skip this step entirely for `meaning_preserving_local`.
3. Read `references/intake-workflow.md`. Resolve the one primary Workflow Profile through the router above without reopening any known goal, then apply its design-ready additions without creating a new questionnaire. For a new build, resolve only the current largest missing decision that would change the report design. For a `meaning_changing` continuation, reuse still-supported decisions and ask only the single largest missing delta that would change the requested result; do not replay the full interview. A clear `meaning_preserving_local` continuation asks no intake questions. For an external conversion goal, distinguish the desired action from its verified real action path; do not impose this requirement on non-conversion reports. Complete ordinary missing scenes, numbers, viewpoints, and expression as creative supplements instead of extending intake. Stop according to the reference's readiness, repetition, information-gain, hard-boundary, and question-budget rules.
4. When several report structures are genuinely reasonable, present 2-3 chapter-level options and let the user choose or delegate. Do not ask about structure when one option clearly follows from the confirmed goal and evidence.
5. After content and structure are clear, resolve the visual source. Read `references/profile-memory.md`; parse the current enterprise identity from eligible material/conversation and resolve only explicit identity candidates against TaoHtml home. A unique active profile automatically selects its active version: run the minimal `profile-reuse` environment profile before binding or loading it, but do not reopen reference images, regenerate VI, launch Chromium, or ask whether to reuse. Show only “本次沿用【企业显示名 企业模板 vN】；如需更换请直接说明” and continue unless the customer objects. Ask exactly one selection question only for several candidates, unclear identity, alias conflict, or a current requirement/profile conflict; never guess or mix companies. If no profile applies or the customer requests a new/permanent template, resolve the ordinary visual route. If the user chooses “use my reference”, identify `reference_mode`. **参考风格重构** accepts exactly one static PNG, JPEG, or WebP screenshot; **企业模板保真** accepts one to three representative static screenshots from the same template family. When intent is still unclear, ask exactly one binary question: **参考风格重构** (extract the design language and allow recomposition) or **企业模板保真** (lock screenshot-visible corporate elements and design only each shell's safe content region). Count this question inside the existing clarification budget. If the user already says “企业模板保真”, “公司模板原样采用”, or an equivalent clear instruction, set `corporate_fidelity` and do not ask again; otherwise preserve the existing `reconstruct` behavior. Read `references/static-reference-vi.md`, run the `static-reference` profile before opening or analyzing any reference image, pass its current-session readability gate, analyze static frames only, fill the shared executable-layout grammar and mode-specific fields, render one unified VI design standards board, and wait for a clear confirmation of the exact current board. Record the current conversation reference; do not require a fixed reply phrase. Both modes use this same dependency chain and confirmation gate. Do not infer dynamic rules, force an internal theme, create a prose-only visual summary, begin project-theme generation, or start formal report production before this confirmation. PPT, webpage, video, state-sequence inputs, more than three corporate screenshots, or multiple screenshots for reconstruct remain unsupported; ask for a supported representative raster input instead of routing them as “no reference.” Only when no clear reference exists and no profile applies, read `references/visual-systems.md`. If the user has already specified one concrete built-in system, adopt it directly without displaying the catalog and record the exact decision reference. Show a category subset only when the user has proactively and explicitly constrained the acceptable range of the built-in catalog and that constraint maps unambiguously to one declared category; never infer a catalog-range constraint from project context. Otherwise, show every system in the complete current built-in catalog in the same round, with each exact customer-facing name, one-line description, and bundled preview; never hide a system because the Agent considers it a weaker fit. Report goal, audience, content, report type, and reading or presentation mode are recommendation inputs only: use them to mark one or two displayed systems as **更推荐**, but never to shrink the catalog; recommendation never replaces complete catalog display. If a user preference or constraint does not map unambiguously to a declared category, show the complete current catalog, reflect that preference in the recommendation reason, and never invent an ad hoc subset. Wait for the user's selection or explicit delegation; the ordinary six-question cap and three-no-gain stop never authorize theme selection. For every visual route, present `minimal | moderate | rich` as **少量 / 适中 / 丰富**, recommend at most one, and likewise wait for user selection or explicit delegation. Record both decisions and references once, never repeat known choices, and never infer motion from a Profile, static input, model judgment, or question-budget stop.
6. On exact profile reuse, write and validate the current task's profile-use binding, resolve its relative theme path through TaoHtml home, and load that theme with the existing project-theme loader before the Report Design Brief. Treat the binding's `target_mode` as the current report Runtime state and pass it to the shared renderer even when it differs from the theme's first-compilation mode; a reading/presentation change alone never creates a profile version. The binding replaces only repeated VI generation; it does not confirm the brief or authorize production. After clear confirmation of the current VI board for a new reference on either static-reference mode, read `references/project-theme-compiler.md`, create its hash-bound handoff, and compile the current project's theme before the Report Design Brief. In `corporate_fidelity`, bind every source page's hash, dimensions, `canvas_bbox`, role, shared crops, explicitly declared replaceable regions, shell-specific locked/editable regions, extension pages, and limitations; deterministically crop and embed fixed elements without model redraw, remove only an authorized variable page-number region before Runtime supplies one page number, keep fixed elements stationary, and route each report page role to its matching shell with Runtime behavior confined to the editable region. Never infer replaceable pixels from a page-number string or coordinate, and never use a complete screenshot as a page background. After the compiled theme passes the existing loader, create enterprise profile v1 only for a new company, or create and atomically activate vN only when the customer explicitly says the company default should change. A current-task-only override writes `temporary_override: true` and never changes the active pointer; another company always uses a separate profile. Do not add any profile result to the eight built-in systems, compile an unconfirmed or changed VI, persist report content in a profile, or infer motion from static inputs. On the no-reference route, keep the selected built-in system instead. Only after the applicable visual/theme/profile gate and the independent theme/motion choices are complete, read `references/design-brief-template.md` and produce one adaptive Report Design Brief. Record the primary Workflow Profile id/name/definition version, semantic selection basis, and bounded capability overlays without adding an IR questionnaire. Record the enterprise profile id/version/binding and temporary-override state when applicable; otherwise record `reference_mode`, source roles, fidelity boundary, locked elements, editable regions, observed/extension/unknown boundary, confirmed VI and compiled project theme when applicable, selected built-in system when applicable, any necessary deviation, and the planned creative-supplement scope. Always record theme applicability, selection/delegation status and reference, plus the native motion density, customer label, selection/delegation status and reference. Workflow Profile selection, VI confirmation, enterprise-profile binding, and design choices are not Report Design Brief confirmation.
7. Wait for explicit confirmation of the current brief. This confirmation does not count toward the clarification-question budget. A previous "agree", "continue", or request to use TaoHtml is not production authorization.
8. Read `references/production-authorization.md`. Record the exact built-in theme decision when applicable and the motion-density decision for every visual route, including `user_selected | delegated_to_taohtml` and the current decision reference; `pending` blocks the brief and every formal action. Before confirmation, save each applicable current material summary, VI board or profile-use binding, and Report Design Brief as a task-local gate artifact; record its safe relative path, current SHA-256, and applicable confirmation trace. Bind a confirmed brief to the checker-generated canonical SHA-256 of the complete normalized built-in-theme/not-required and motion-decision objects; never preserve that confirmation after any bound value, status, or decision reference changes. Run `scripts/check_production_authorization.py --artifact-root <current-task-root> --action formal-html`. Only a successful current-file check authorizes formal HTML; rerun it before browser QA and delivery so any post-confirmation byte, active-profile, version, identity, theme, or recorded design-choice change fails closed until the affected gate and brief are rebuilt. A bound-material summary preview, static-reference VI standards-board preview, profile binding, design-choice prompt, and Report Design Brief remain allowed only in their matrix states; none is a formal report preview. After authorization, read `references/process-playbook.md` and produce the HTML directly. Do not insert a separate full prose manuscript step. Follow its **first runnable artifact** cadence: lock a concise page plan, save a complete runnable `index.html`, then refine and QA in bounded passes. On static-reference or profile-reuse routes, explicitly load the validated project theme through the shared renderer; never substitute one of the eight built-in themes.
9. Implement only the runtime capabilities documented in `references/runtime-contract.md` unless the user separately authorizes new runtime engineering.
10. Run asset QA, then run the `browser` profile before browser QA. Fix objective failures and report the files, checks, and production-stage judgment calls. Until the current minimum readiness checks pass, say only that an artifact was found or can be previewed; do not call it ready or formally deliverable. Derive operating instructions from the exact current HTML tested in browser QA or from the current Runtime contract, clearly distinguishing generic Runtime behavior from artifact-tested behavior. Deliver the usable report together with the concise `《待核实内容清单》` defined in `references/process-playbook.md`; do not withhold the report merely because ordinary creative supplements still await customer verification.

If the user adds source material or changes real data, evidence relationships, a core viewpoint, structure, scope, or responsibility after confirming the brief, rebuild the affected source interpretation and brief fields, display the complete current brief, and request confirmation again. A post-delivery local copy, color, layout, technical, portability, or motion revision that preserves meaning and structure does not rerun intake, material summary, or brief confirmation; it still requires applicable QA and delivery verification on the exact current artifact.

## Question Discipline

Maintain the `known | confirmed | inferred | missing` ledger defined in `references/intake-workflow.md`. Re-read the conversation, sources, and prior answers before every question; never ask the user to repeat known or safely inferable information.

A read-only handoff uses the zero-question audit in `references/project-handoff.md`
instead of this intake. A clear meaning-preserving local continuation also asks no
intake questions. For meaning-changing continuation, preserve every still-supported
ledger item and apply the same six-question maximum only to the remaining delta.

Ask one decision question per round: the current largest missing item whose answer could change the report design. Do not bundle independent startup choices or turn the intake into a fixed questionnaire.

A clear input may need 0 clarification questions; ordinary intake should usually finish in 3-5; even the most complex idea-only intake must never exceed 6 agent-initiated clarification questions in one intake cycle. Ask about the same key gap at most twice, changing the second attempt to a concrete example or 2-3 real options. Stop as soon as the project is design-ready, and stop questioning after three consecutive rounds without actionable new information.

Infer reversible ordinary design decisions transparently and place them in the brief for confirmation. Never infer built-in theme or motion density without explicit delegation. Complete ordinary missing scenes, numbers, viewpoints, and expression during production, track them as `creative supplement | projected content | illustrative content | pending verification`, and disclose them at delivery. Do not describe these customer-facing categories as fabrication or hallucination.

The one-time reference-mode choice is a clarification question, not a new gate or extra budget. Ask it only when the user's intent is genuinely ambiguous; never repeat it after the mode is known. Built-in theme and motion-density choices are a separate design gate outside the clarification count; they remain required after six ordinary questions and are not skipped by three no-gain rounds.

Block only on the hard boundaries in `references/intake-workflow.md`: never invent a real customer or company identity, quotation, citation, literature, or source; never present an illustrative case as an achieved customer outcome; require explicit verification for legal, medical, financial, safety, and similar high-risk facts; and never replace confirmed real sources, data, or action channels. Treat "decide for me", "not important", or equivalent wording as delegation. A user-initiated change to the core goal or scope starts a new intake cycle rather than a seventh question.

## Source And Meaning Protection

- Use a local file only when it is a current accessible upload, a resolvable exact path the user provides, an accessible source explicitly bound by the current task instruction, or an exact candidate the user confirms after explicitly asking TaoHtml to find it in a narrow in-scope directory. A conventional filename such as `input/prompt.md`, current working directory placement, workspace presence, or historical task residue is not a binding.
- For every material actually used, record its path, upload identity, or exact external locator; `source_binding`; source role; availability status; evidence-verification status; inspection coverage; and binding reason in the applicable source ledger and, when a brief is required, the Report Design Brief. Keep original customer material, external public evidence, secondary handoff summaries, current artifacts, visual references, Agent-generated material, and described-but-unavailable material distinct. Use `agent_retrieved_external | external_public_evidence | external_retrieved_inspected` only for current-task external retrieval with exact provenance; never use it for a local candidate. Do not read an unbound candidate merely to decide whether it is useful.
- Candidate discovery is disabled by default. A route number, workspace scope, or current working directory is not search authorization. Only after the user explicitly asks TaoHtml to find the file may it inspect metadata in a narrow directory the user specified or clearly placed in scope, show exact candidate paths, and wait for confirmation without reading content. Never broadly scan user directories. A shell lookup that finds nothing does not prove that material was cleaned, deleted, or permanently lost.
- You may reorganize, compress, and improve expression, but preserve every confirmed core viewpoint.
- Separate source facts from interpretation.
- Keep creative supplements distinct from source facts without treating the supplements as automatic errors.
- Resolve contradictions that affect the conclusion before the design brief is confirmed.
- Use customer screenshots, photographs, logos, and documents as real material; do not regenerate them as fictional substitutes.
- In `corporate_fidelity`, preserve only screenshot-visible fidelity. Do not promise recovery of the original PPT master, vector Logo, font files, or unseen assets. Never ask a model to redraw a Logo; when every supplied screenshot is insufficient for deterministic extraction, request a clearer screenshot.
- Do not rename customer-provided or independently verified facts as creative supplements. Preserve their provenance and exact confirmed meaning.
- Keep public evidence and automatic data corrections visible in the design brief's source and confirmation sections.
- Treat faithful migration versus redesign as a source-handling strategy, not as a substitute for choosing reading versus presentation mode.

## Production Routing

After brief confirmation, load only what the task needs:

The Report IR path is TaoHtml's supported, deterministic engineering route. Enter it
when the user explicitly asks to research, generate, validate, compile, benchmark, or
continue a Report IR project, or when the current project has an explicit Report IR
authorization. Do not silently move an ordinary customer build from the confirmed
direct-HTML workflow onto Report IR: Direct HTML remains the default production route.
For an authorized Report IR build, read `references/report-ir-pilot-workflow.md`; do
not ask the customer to select IR or add an IR questionnaire. For other explicit
Report IR engineering work, read
`references/report-ir-v1.md`, validate the exact IR with
`scripts/validate_report_ir.py`, then compile it with
`scripts/compile_report_ir.py`. The Compiler never replaces the Report Design Brief or
production-authorization gates and never calls a model. If the customer edits an
IR-compiled HTML, use `scripts/apply_report_ir_patch.py` to bind the exported Runtime
Patch back to the exact base IR. Classify the edit as meaning-preserving or
meaning-changing; never compile a meaning-changing draft until the refreshed brief is
confirmed.

- `references/project-handoff.md`: task-intent overlay, source role/availability map, read-only audit, continuation boundaries, candidate discovery, and readiness language.
- `references/project-handoff-schema.md`: portable workspace/project/snapshot identities, strict source/decision/design/artifact/lineage serialization, version policy, and four-layer handoff validation.
- `references/workflow-profile-contract.md`: one-primary-Profile contract, direct definition routing, horizontal-parameter boundary, capability overlays, IR isolation, and existing-gate preservation.
- `references/workflow-profiles.md`: lightweight nine-option catalog for ambiguous routing only; after selection, load only the unique definition reference named by the selected row.
- `references/process-playbook.md`: story, evidence, visual, production, and delivery workflow.
- `references/layout-pattern-library.md`: layout selection for composed presentation pages.
- `references/visual-systems.md`: built-in system routing and selection policy; after selection, load only that system's `theme.json`, `theme.css`, and `templates.html` under `assets/visual-systems/`.
- `references/static-reference-vi.md`: one-time reconstruct/corporate-fidelity routing, supported static-input gate, observed/extension/unknown boundary, exact executable layout grammar, corporate template-family contract, unified VI board, confirmation gate, and next-step handoff.
- `references/project-theme-compiler.md`: post-confirmation hash-bound handoff, deterministic structural project-theme compilation, corporate multi-shell crop generation and role routing, eligible/compiled usage mapping, fallback policy, explicit project rendering, and verification.
- `references/report-ir-v1.md`: formal report-source contract, semantic/evidence/page/state model, four independent validation results, deterministic Compiler boundary, project-theme routing, and implemented capability limits. Load only for the explicit Report IR engineering route above.
- `references/report-ir-pilot-workflow.md`: explicit Report IR routing, confirmed-brief derivation, no-fallback deterministic orchestration, existing QA/Handoff reuse, and machine-checkable not-executed states. Its legacy filename and machine field names are retained for compatibility.
- `references/profile-memory.md`: explicit TaoHtml home, exact enterprise resolution, immutable corporate-profile versions, automatic binding, override/update/other-company semantics, export/import, and current-task authorization boundary.
- `references/design-quality-rubric.md`: optional diagnosis when the user asks for a design review or says the result feels ordinary; do not use a fixed aesthetic score as the production authorization gate.
- `references/runtime-contract.md`: implemented DOM, controls, state, modes, and extension boundary.
- `references/content-editor.md`: lightweight text/image revision, lock hooks, unified history, session recovery, honest export boundary, and browser QA.
- `references/environment-preflight.md`: capability profiles, standard-library launcher, timing, JSON contract, dependency declaration boundary, and fail-fast recovery choices.
- `references/production-authorization.md`: current-task gate state, allowed-action matrix, preview boundary, and machine check before formal HTML or delivery.
- `assets/html-deck-template/`: dependency-free 16:9 starting shell for paged reading and single-screen presentations.

Use the bundled scripts where relevant:

- `scripts/extract_pdf_pages.py`: render PDF pages into evidence assets.
- `scripts/preflight.py`: run `core`, `pdf`, `static-reference`, `profile-reuse`, or `browser` capability checks before the corresponding work. Its parent process uses only the Python standard library.
- `scripts/profile_store.py`: create, update, list, show, resolve, bind, validate, activate, rollback, archive/restore, export, and import explicit corporate-template profiles without writing to the Skill directory.
- `scripts/check_production_authorization.py`: validate current material-summary, VI or profile-use binding, project-theme, and design-brief state before a requested preview, formal HTML, QA, or delivery action.
- `scripts/validate_project_handoff.py`: validate a structured portable handoff's schema, exact bindings, continuation state, and recorded delivery evidence without executing QA.
- `scripts/validate_report_ir.py`: validate Report IR schema, references, semantics, and current compiler readiness separately; it never executes QA.
- `scripts/orchestrate_report_ir_pilot.py`: preserve direct HTML by default, or validate an explicitly authorized Report IR project and bind Production Authorization, Report IR validation, local Compiler outputs, and existing Handoff records without generating content or claiming QA execution. Its legacy filename is retained for compatibility.
- `scripts/compile_report_ir.py`: deterministically compile a validated Report IR through a built-in theme or validated project theme into Runtime HTML, Source Map, normalized IR, and Build Manifest without model calls.
- `scripts/apply_report_ir_patch.py`: extract or load a controlled Runtime text/image Patch, verify its exact base binding and before-values, update Report IR and image provenance, and stop with a reconfirmation gate when meaning changes.
- `scripts/check_assets.py`: find missing, remote, or non-portable assets.
- `scripts/check_html_deck.py`: exercise routes, reveal states, runtime behavior, media, console errors, bounds, and screenshots.
- `scripts/build_contact_sheet.py`: build a visual QA overview.
- `scripts/package_deck.py`: package HTML plus local assets when a single file is not appropriate.
- `scripts/render_visual_system.py`: render content through one built-in id or an explicit `--project-theme` directory while retaining the shared runtime shell. Pass a real local source image as `--source-kind verified`; verified provenance is never inferred from a local path. If `source_kind` / `--source-kind` is omitted, the Python API and CLI default to `illustrative` even when a local image is supplied. When no real evidence image exists, use the renderer's automatically labeled illustrative placeholder or pass a local image as `--source-kind illustrative`. The renderer never labels illustrative material as verified evidence.
- `scripts/render_reference_vi.py`: validate legacy reconstruct v1.1, single-reference v1.2, or corporate-family v1.3/v1.4; verify source hashes, static frame counts, canvas crops, normalized fixed/editable/replaceable regions, and strict 16:9 tolerance; extract deterministic fixed crops; render the standards-board HTML; and export a 3200×2400 PNG. It does not analyze images or compile a project theme.
- `scripts/compile_project_theme.py`: validate the exact confirmed-VI handoff and shared executable-layout compatibility matrix, then deterministically write project-local manifest, CSS, templates, and provenance. Corporate-family mode embeds only hashed fixed crops, emits stationary role-specific shells, and wraps report content in the matching editable region. It does not call a model or add a built-in theme.

## Current Runtime Boundary

The standard template supports paged reading, single-screen presentation, and the bundled lightweight content editor documented in `references/content-editor.md`. It does not promise a browser-based PPT editor, free layout changes, chart/table-structure editing, animation editing, dual-screen presenter view, cross-page morphing, durable version history, or browser ZIP export.

## Delivery Gate

Before delivery:

- Build a brief-to-output traceability ledger and verify every confirmed core viewpoint, correction, evidence gap, and decision boundary against a visible output location. On a meaning-preserving local continuation, verify the same meanings against the exact delivered baseline instead of inventing a new brief. For conversion reports, also verify that the real action path is visible, usable, aligned with the desired action, and consistent with its recorded source and verification status. Check every conjunct in compound requirements; a source screenshot may support a point but must not silently replace it in the designed narrative.
- Check all local and remote asset references.
- Exercise reading and presentation modes, step navigation, whole-page navigation, return-state preservation, and hash routes.
- Check console errors and visible bounds at the target viewport.
- Prefer a single self-contained HTML when it stays responsive; otherwise deliver `index.html + assets` as a zip.
- Deliver `《待核实内容清单》` after the report. Each entry must locate the page/content, name the supplement type, state the source status, and recommend `confirm | modify | delete | ask TaoHtml to replace`. Do not collapse the list into a generic disclaimer.
- Keep ordinary projected content in the delivery note so the presentation remains clean. Add an adjacent `示意 / 模拟 / 待核实` label inside the HTML only for simulated charts, fictional customer cases, generated evidence-like artifacts, or data likely to be mistaken for real proof.
