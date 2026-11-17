# PPT-Like Report Building Playbook

This playbook generalizes a complete collaborative process for turning loose materials, screenshots, demos, and business intent into a polished PPT-like report or HTML presentation.

Use it after the current Report Design Brief has been confirmed for a new build or
meaning-changing continuation. A meaning-preserving local continuation may use only
the bounded revision and QA/delivery parts of this playbook without a new Material
Understanding Summary or Report Design Brief confirmation. Intake, material-summary,
and confirmation rules live in `intake-workflow.md` and
`material-understanding.md`; do not restart them here.

For an inherited project, read `project-handoff.md` before using this playbook. A
`review_only` handoff stops before production and does not use this playbook to create
HTML. A `continue_existing` task begins from the exact current artifact and follows
the Continuation Decision Matrix there. Do not treat the handoff narrative as
original evidence or replay the full interview.

For a new build or meaning-changing continuation, require a successful
`scripts/check_production_authorization.py --action formal-html` result for the current
task state in `production-authorization.md` before saving the first runnable formal
`index.html`, and require `--action deliver-formal-html` before delivery. An existing
file or earlier task state is not evidence of current authorization on that path. A
meaning-preserving local continuation does not manufacture a new authorization state
or first-runnable artifact: preserve the exact delivered baseline, keep the revision
inside its semantic boundary, and run the applicable asset, browser, Runtime/editor,
traceability, and delivery checks on the exact result.

It is not tied to any single topic. Use it for salon decks, training courseware, sales proposals, consulting reports, diagnostic reports, product presentations, investor-style narratives, internal strategy decks, and other slide-based reports.

## 1. Start With The Real Objective

The first question is not "how many slides". The first question is:

> What decision, belief, or action should the audience reach after this report?

Keep the desired action separate from its execution path. For a conversion objective, production may use only the exact channel and verification status recorded in the confirmed brief; a persuasive verb is not a substitute for a usable entry point.

Clarify:

- Who is the audience?
- What problem do they already feel?
- What do they misunderstand?
- What proof would change their mind?
- What action should they take next?
- What time or depth constraint is already recorded in the brief, if any?

For a live talk, the deck should support rhythm and persuasion. For a report sent after the meeting, it should support independent reading. For a product proposal, it should reduce buying risk. These are different documents even when the topic is the same.

## 2. Build The Story Spine Before Writing Slides

Do not begin by filling pages. First create a story spine.

A persuasive commercial spine often follows this movement:

1. **Current behavior**: something in the audience's world has changed.
2. **Visible example**: show that change through a concrete case.
3. **Risk**: explain what happens if the audience ignores it.
4. **Definition**: name the new concept after the pain is visible.
5. **Mechanism**: explain why it happens.
6. **Framework**: compress complexity into usable categories.
7. **Evidence or projection**: show real proof when available; otherwise make the reasoning explicit and track creative supplements for verification.
8. **Operating model**: turn the idea into a repeatable process.
9. **Offer**: show how the presenter can help.
10. **Boundary**: clarify what is promised and what is not.
11. **Closing action**: give the audience a clear next step.

Do not force offer, pricing, sales, or CTA pages into research, internal, educational, or neutral reports. Select the roles that serve the confirmed goal.

When a user gives a rough outline, preserve the intent but test whether the order earns the conclusion. If the conclusion appears before the proof, move it later or add evidence earlier.

## 2A. Choose The Output Mode For Existing Source Material

When the input is a PDF, PPT, existing HTML deck, screenshots, or a long report, make an explicit mode decision before design work.

### Faithful Migration

Use this mode when the task is essentially "make this portable, browsable, searchable, or presentable without losing layout."

The main surface can preserve the source page image. Improvements live in the shell:

- Keyboard navigation.
- Thumbnail overview.
- Text extraction panel.
- Zoom or source view.
- Portable asset folder.
- Downloadable original.
- Page count and hash routing.

This is not a redesign. Do not claim that it is.

### Roadshow Redesign

Use this mode when the user asks for a roadshow, redesign, better design sense, a style like an existing deck, animation, stronger storytelling, or says the faithful version is too ordinary.

In this mode:

- The source is raw material, not the layout.
- Extract every important fact, number, chart, and relationship.
- Build a new page role sequence.
- Create a visual metaphor.
- Use the original source pages as evidence modals, appendix pages, thumbnails, or "source" buttons.
- Rewrite the information as scenes, systems, contrasts, process flows, data maps, or case teardowns.

If the redesigned page still looks like "title + three cards + small text", it is probably not roadshow quality.

## 2B. Continue A Handed-Off Project

Before editing, build or reuse the source-role and availability map from
`project-handoff.md`. Record the exact current artifact, what was inspected, what is
known only from a secondary summary, what came from retrieved public/third-party
evidence, and what is unavailable or unverified. A current HTML is the baseline for
rendered behavior and wording; it is not automatic proof of the source, evidence
relationship, or correctness of its claims.

Continue layout, typography, color, technical behavior, portability, local assets,
and meaning-preserving local expression when the requested delta stays inside those
boundaries. This `meaning_preserving_local` path does not rerun intake, rebuild a
Material Understanding Summary, or generate/reconfirm a Report Design Brief. Preserve
the exact delivered baseline and run current artifact QA and delivery verification
after the change.

Use the `meaning_changing` path before modifying real data,
quotation/citation/source attribution, evidence-to-claim relationships, real
identities or achieved outcomes, a core conclusion, chapter structure, scope promise,
or responsibility boundary. Restore the original source or obtain explicit
confirmation of the exact change, rebuild only affected source/brief fields, display
and confirm the complete current brief, then apply the current authorization and QA
gates. Apply the existing high-risk verification rules even after user confirmation.

Ordinary missing scenes, examples, projected values, viewpoints, and expression still
follow output-first production. Track them as creative supplements and deliver them in
`《待核实内容清单》`; do not block every continuation because some original material is
unavailable.

## 3. Use Chapter Grammar

A deck becomes easier to follow when every chapter has a recognizable shape.

Recommended chapter structure:

- **Opener**: one proposition. Big type. Low density. It tells the audience what new part starts now.
- **Demonstration / proof**: real material that lets the audience see the point.
- **Explanation**: what the proof means.
- **Framework / method**: how to act on the explanation.
- **Closing / hinge**: what we have now established, and why the next part is necessary.

Typical chapter opener:

- "The customer behavior has changed."
- "The problem is not content volume; it is evidence quality."
- "This is an engineering problem, not a one-off content task."

Typical chapter closing:

- "So far we have proven the risk."
- "Now the question becomes: how do we make this repeatable?"
- "This is why the next section must talk about process, not just ideas."

## 4. Give Every Slide One Job

Before designing any slide, assign a role:

- **Cover**: creates first impression and names the offer or topic.
- **Opening proposition**: sets the mental frame.
- **Simulation**: shows a user behavior or system behavior.
- **Evidence**: displays source material.
- **Diagnosis**: names the gap.
- **Definition**: explains a concept.
- **Mechanism**: shows how something works.
- **Framework**: gives categories the audience can remember.
- **Case**: proves the framework with real details.
- **Workflow**: shows repeatable execution.
- **Tool / system**: makes the process tangible.
- **Boundary**: prevents overpromising.
- **Pricing / offer**: turns interest into action.
- **Closing**: lands the final message.

If a slide tries to define, prove, sell, and teach at the same time, split it.

## 5. Turn Claims Into Evidence Pages

A claim without proof should become a hypothesis, receive evidence, or be completed as a clearly tracked creative supplement. The third path keeps production moving; it does not turn generated content into source evidence.

Useful evidence types:

- Real screenshots.
- Source documents.
- AI answer examples.
- Customer messages.
- Tables and metrics.
- Before / after comparisons.
- Process recordings.
- Generated reports.
- Media coverage.
- Certificates, credentials, or third-party proof.
- Product interfaces.
- Pricing or service package images.

How to convert evidence into a slide:

1. Keep the original artifact visible.
2. Crop for readability, not decoration.
3. Use callouts to guide the eye.
4. Add only enough interpretation to make the evidence useful.
5. Avoid rewriting the source into vague summary.

When a report screenshot is long, split it into slices:

- Overview / header and methodology.
- Core metrics.
- Data visualization.
- Case detail or raw samples.
- Final diagnosis or conclusion.

Do not omit data visualizations if the user says the report itself is important. Visual charts often carry credibility that summaries cannot replace.

During production, keep a creative-supplement ledger with four fields: page/content location, supplement type, source status, and suggested customer action. Ordinary projected narrative can stay visually clean and be disclosed in the delivery note. A simulated chart, fictional customer case, generated evidence-like artifact, or data display likely to be mistaken for real proof must also carry an adjacent `示意 / 模拟 / 待核实` label in the HTML. Never give a fictional case a real customer or company identity, fabricate a quotation/citation/source, present it as an achieved customer result, or replace confirmed source data.

## 6. Design A Deck-Level Visual System

A good presentation should feel like one designed object.

Define the system once:

- **Color**: primary background, text, accent, warning color.
- **Type**: large title scale, compact label scale, body scale.
- **Grid**: margins, columns, major alignment lines.
- **Motifs**: rulers, dot matrices, dashboards, paper fragments, labels, terminals, report cards, circular cutouts, timelines.
- **Density rhythm**: alternate between low-density opener pages and high-evidence pages.
- **Media treatment**: screenshots, videos, reports, diagrams, posters, QR codes.

Design should match the domain:

- Business reports should feel controlled, precise, and evidence-led.
- Training decks should feel clear and progressive.
- Sales decks should feel credible before they feel promotional.
- Product/tool decks should show the actual tool as early as possible.
- Workshop decks need more interaction and staged reveals.

Avoid decorating pages before the slide role is clear.

For high-design roadshow work, load `design-quality-rubric.md` and `layout-pattern-library.md` before implementation. The rubric defines the quality bar; the layout library prevents repeated generic card pages.

## 6A. Extract Design DNA From A Reference Deck

When the user says a previous deck "has design sense" or asks to follow a reference style, do not copy only colors. Extract the behaviors that create the effect.

Checklist:

- **Composition**: Is the design symmetric, asymmetric, full-bleed, poster-like, dashboard-like, or stage-like?
- **Scale**: Does it rely on huge headlines, dense micro-labels, oversized numbers, or dramatic contrast?
- **Surface system**: Does it use light paper, black panels, glass panes, report windows, source cards, terminal panels, or cutaway diagrams?
- **Motifs**: Does it use grids, ruler marks, dot matrices, circular cuts, arrows, labels, geometric blocks, magnifiers, evidence tags?
- **Color behavior**: Which color is background, which is accent, which signals risk or conclusion?
- **Evidence behavior**: Are screenshots embedded, cropped, floated, magnified, animated, or shown in a modal?
- **Motion grammar**: Does the deck reveal serially, zoom into cards, type text, scroll reports, or open live demo panels?
- **Tone**: Does it feel premium, urgent, technical, institutional, product-like, editorial, or operational?

After extraction, write a one-paragraph design thesis for the new subject.

Example:

> This report should feel like a "data factory cutaway": manual reports enter on the left, standardized data assets accumulate in the center, and BI/AI use cases leave on the right. Use dark operational panels, oversized red problem statements, champagne-gold signal lines, source-page evidence modals, and staged reveals.

The thesis is more important than the palette. A weak thesis produces a generic business deck even with good colors.

## 7. Build Interaction For The Presenter

Live decks must follow the speaker's click rhythm.

If a slide has multiple ideas, use serial stages:

1. Title appears.
2. First object appears.
3. First object is explained.
4. Second object appears.
5. Comparison or conclusion appears.
6. Final click moves to the next slide.

Important rule:

> If the presenter uses a clicker, every important reveal must be reachable by the same forward action.

Avoid:

- Hidden hover effects.
- Click targets that require precise mouse placement.
- A modal that auto-plays before the presenter is ready.
- Pages that jump to the next slide before the final stage is visible.

For video, only when the user separately authorizes video work and the output runtime implements it:

- Default to a poster or still frame.
- Open the video in a modal when clicked or when the staged reveal reaches it.
- Match the modal ratio to the video ratio.
- Provide replay and return.
- Stop playback when leaving the slide.

For report previews:

- Use an auto-scroll panel only if the user wants a "live report" feeling.
- Otherwise split the report into readable slices across pages.

## 8. Implement HTML Decks Safely

HTML decks are useful when the presentation needs rich motion, simulations, report previews, or interactive staged reveals. The current standard runtime does not promise video behavior.

Implementation rules:

- Use `assets/html-deck-template/` as the starting shell when creating a new HTML deck from scratch.
- Keep HTML, CSS, and JS in the same file or a controlled local folder.
- Avoid external dependencies unless there is a clear reason.
- Use CSS variables for visual system consistency.
- Use stable 16:9 slide dimensions.
- Test at 1366x768, 1600x900, and 1920x1080, plus the user's actual browser scale when needed.
- Preserve keyboard navigation and hash定位.
- Preserve each slide's staged state when leaving and returning.
- Keep page count accurate.
- Do not break existing navigation while adding slide-specific behavior.

Asset rules:

- Do not leave references pointing to random Desktop, WeChat cache, temp, or absolute local paths if the deck must travel.
- Copy images, posters, and report files into a local `assets/` folder.
- Prefer relative paths.
- Create a portable zip when the user wants to use another computer.

Recommended local tool flow:

1. Render PDF pages with `scripts/extract_pdf_pages.py` when original source pages are needed as evidence.
2. Build or edit the HTML deck using the template or existing deck shell.
3. Check portability with `scripts/check_assets.py`.
4. Run the `browser` profile in `environment-preflight.md`; only after it passes, run browser QA with `scripts/check_html_deck.py`.
5. Create a contact sheet with `scripts/build_contact_sheet.py`.
6. Package the folder with `scripts/package_deck.py`.

### 8A. Land The First Runnable Artifact Early

After the brief is confirmed, or after a meaning-preserving local revision is
classified against an exact delivered baseline, production should become visible
quickly. Do not spend a long uninterrupted phase repeatedly reconsidering layouts,
assets, or optional features before any runnable file exists.

Use this sequence:

1. Write a concise page plan: page role, core claim, evidence, layout family, and staged-state count where relevant.
2. Lock one design thesis and the recurring visual motifs. Reopen that decision only when implementation exposes a concrete failure.
3. For a new build, instantiate `assets/html-deck-template/`; for continuation, work from a controlled copy of the exact bound current artifact and preserve its unmodified baseline identity. Then save a complete runnable `index.html` with every planned page, navigation, and essential content present. A simple but coherent first pass is preferred to a half-built high-detail page.
4. Add evidence, creative supplements, and visual refinement in bounded passes. Embed or render only the source pages needed to support visible source claims; do not package the entire source by default. Add every actual creative supplement to the delivery verification ledger as it is introduced.
5. Run asset QA as soon as the runnable artifact exists. Run the `browser` preflight before browser QA, and fix objective failures before adding optional polish. A failed or unavailable browser profile is not a passed browser-QA result.
6. Stop when the confirmed scope, visual direction, runtime contract, and delivery gate are satisfied. Do not add unrequested pages, controls, or runtime features during refinement.

The first runnable artifact is not the final quality bar. It is the production checkpoint that keeps the work inspectable, testable, and recoverable while design quality is improved.

## 9. Write Speaker Notes After Structure Stabilizes

Speaker notes should follow the slide, not replace it.

For each page:

- Name the page number and title.
- Write a natural opening line.
- Explain the main point in spoken language.
- Tell the presenter what to emphasize.
- Add a transition sentence.

For opener pages, write short transition language.

For evidence pages, describe:

- What the audience should notice first.
- Why this evidence matters.
- What conclusion can be drawn.
- What cannot be overclaimed.

For commercial closing pages, make the next action concrete without overselling.

## 10. Close With Offer, Boundary, And Executable Action

A report that promotes a product, service, or tool should not end abruptly after the framework.

Recommended closing stack:

1. Summary of what the audience now understands.
2. The practical problem that remains.
3. The system, tool, or service that solves it.
4. What is included.
5. What is not promised.
6. Pricing or package, if relevant.
7. Clear next action.

For a conversion report, make the next action executable:

- Copy the exact verified action path from the confirmed brief. Never synthesize a placeholder channel or “improve” a URL, command, contact detail, price, or product entry from memory.
- Show the complete path visibly enough to use. A button label, a generic three-step slogan, or “scan/contact/try now” without the underlying link, syntax, command, or contact route does not close the action.
- Make a link's destination match the visible verified URL. When using a QR code, encode the same verified value, decode the rendered code during QA, and keep a readable text alternative on the page.
- Validate usability without taking the external action: open public URLs and confirm the intended destination; compare host-agent syntax or commands with authoritative documentation or project context; compare contact details and prices with their confirmed source. Do not submit a form, send a message, place an order, or create an account merely to test a CTA.
- If production reveals that the confirmed path is missing, incomplete, or invalid, return to intake and revise the brief. Do not ship a direct-action claim with an implied or fictional route.

For reports without a conversion objective, do not add a CTA channel or closing sales page merely to satisfy this section.

Boundary language is important:

- Promise process, evidence, diagnosis, construction, review, and iteration.
- Avoid promising guaranteed rankings, guaranteed recommendations, guaranteed conversion, or platform behavior outside your control.

## 11. Package For Delivery

Before sending or using the deck on another computer:

- Open the final file locally.
- Check all assets.
- Check the first page, complex interaction pages, media pages, and final page.
- Zip the HTML and its asset folder together.
- Give the user the zip as the portable artifact.

Do not call an inherited artifact ready merely because it exists or opens. Before
`ready` or `formally deliverable`, require the current applicable authorization,
strict asset check, browser preflight and HTML QA, brief-to-output traceability, and
delivery verification handoff. Until then, use `found`, `can be previewed`, or `not
yet verified`.

Write operation instructions only after testing the exact current HTML controls, or
from the generic current `runtime-contract.md`. In the latter case, state explicitly
that the handed-off artifact has not yet been verified to implement that behavior.

If the output is PPTX or PDF, still preserve the working source and raw assets separately.

### 11A. Deliver The Verification Handoff

Complete the report first, then include a concise `《待核实内容清单》` in the delivery message. Do not replace the list with a generic disclaimer. Use one row per reviewable supplement:

```markdown
## 《待核实内容清单》

| 页面/内容 | 补充类型 | 来源状态 | 建议动作 |
|---|---|---|---|
| 第 3 页「检索到提案」流程中的“5 分钟” | 推演数字 | TaoHtml 创作性补全，尚待客户核实 | 确认该量级；或修改、删除、让 TaoHtml 改为不含数字的表达 |
| 第 5 页顾问转化场景 | 示意案例 | 合成场景，不代表已发生的客户成果 | 确认场景是否贴近业务；或提供真实案例替换 |
```

Use the source-status column precisely: `用户已提供`, `来源材料`, `公开来源已核实`, or `TaoHtml 创作性补全，尚待客户核实`. Do not put confirmed real data, sources, quotations, or action channels in the creative-supplement category. If no creative supplements were added, keep the heading and state `无；本报告未新增待客户核实的事实性内容`.

## 12. QA Checklist

Content:

- Does the deck have a clear audience and desired action?
- Does every section open and close cleanly?
- Does each slide have one job?
- Are major claims backed by evidence?
- Are ordinary creative supplements separated from source facts and covered by `《待核实内容清单》`?
- Are simulated charts, fictional cases, generated evidence-like artifacts, and easily mistaken data labeled `示意 / 模拟 / 待核实` next to the content?
- Are customer-provided and verified facts preserved with their real provenance rather than listed as creative supplements?
- Is retrieved public/third-party evidence recorded as `external_public_evidence` with `external_retrieved_inspected` and an independent verification result, rather than as customer material or Agent-generated content?
- Does a brief-to-output traceability check map every confirmed core viewpoint, correction, evidence gap, and decision boundary to a visible output location?
- For conversion reports, does executable-action traceability map the desired action, exact path, source and verification status, and final display location from the brief to the output?
- Is the rendered action channel visible, usable, and aligned with the confirmed objective rather than reduced to CTA wording alone?
- If the CTA uses a link, command, contact route, price, or QR code, does its rendered value exactly match the verified source, and does the QR decode to the same path?
- Do compound requirements preserve every required part, such as "SLA, responsibility boundary, and API dictionary" rather than compressing the list into a narrower substitute?
- Is the offer introduced only after the problem and method are credible?
- For continuation, are original material, external public evidence, secondary summary, current artifact, visual reference, Agent-generated material, and described-but-unavailable material kept in distinct source roles and availability states?
- Do meaning-changing revisions to real data, provenance, evidence relationships, or core conclusions have restored sources or exact explicit confirmation?
- Did a meaning-preserving local revision avoid reopening intake/material-summary/brief confirmation while still running applicable checks on the exact resulting artifact?

Design:

- Is the visual system consistent?
- Are adjacent pages visually distinct when their roles differ?
- Are dense evidence pages balanced by low-density opener pages?
- Are screenshots readable?
- Are warnings, conclusions, and CTAs visually differentiated?

Interaction:

- Can the whole deck be operated with a clicker?
- Do staged reveals advance in the right order?
- Does a staged page show its final complete state before leaving?
- Do pages restore their prior reveal state when returning?
- Do step navigation and whole-page navigation remain distinct?

Technical:

- Did the required environment profile pass before each gated material/QA path, with its JSON result preserved when possible?
- Does the deck render at 1366x768, 1600x900, and 1920x1080?
- Is the page count correct?
- Are hash links and page indicators correct?
- Are there missing assets?
- Does the portable zip work on a different path?
- Are readiness statements limited to checks that passed on the exact current artifact?
- Do operating instructions cite `current_artifact_tested` or clearly labeled `current_runtime_contract` evidence rather than an untested handoff assertion?

Optional high-design diagnosis when the user requests it:

- Does the deck clear all hard gates in `design-quality-rubric.md`?
- Which weak dimensions in `design-quality-rubric.md` should be revised first?
- Do not treat a numeric aesthetic score as production authorization or as a substitute for objective QA.

## 13. Common Failure Patterns

### The Deck Starts With Abstract Concept

Fix: start with a behavior, scene, question, screenshot, or contradiction. Define the concept only after the audience feels the problem.

### There Is No Evidence

Fix: ask for or locate screenshots, reports, customer examples, product interfaces, metrics, or demo recordings only when the missing proof changes a hard boundary or conclusion. Otherwise complete the report with a hypothesis or creative supplement, track it for the delivery list, and clearly mark evidence-like simulations in the HTML.

### Two Pages Look The Same But Mean Different Things

Fix: change the layout role. Use a bold opener, a report slice, a diagram, a comparison, or a workflow instead of repeating the same card pattern.

### The Case Page Is Just A Screenshot Dump

Fix: crop the screenshot, add a title, mark the decisive area, and write the implication.

### The Sales Part Arrives Too Early

Fix: move pricing and service pages after diagnosis, mechanism, proof, and operating system.

### The CTA Names An Action But Provides No Route

Fix: distinguish the desired action from its real execution path. Use only the verified channel in the confirmed brief, make the complete value visible and usable, and trace it through delivery QA. If no verified channel exists, return to intake or explicitly downgrade the goal instead of writing a conversion slogan.

### The Interaction Requires A Mouse

Fix: convert reveals into the global next-action sequence so a clicker can operate them.

### The HTML Opens But Images Are Missing On Another Computer

Fix: copy all assets into the output folder, rewrite paths to relative paths, and create a zip containing the whole folder.

### The Handoff Summary Became The Source Of Truth

Fix: restore the role/availability map. Treat the summary as secondary orientation,
the current artifact as rendered state, and original customer material as source
evidence. For a meaning-changing edit, recover the original source or obtain exact
confirmation within the boundary in `project-handoff.md`.

### A Found Artifact Was Reported As Ready

Fix: report only `found` or `can be previewed` until current authorization, asset QA,
browser QA, traceability, and delivery checks pass. Do not repeat control instructions
from the handoff without testing the artifact or labeling them as generic current
Runtime-contract behavior.

### The Speaker Notes Sound Like Written Text

Fix: rewrite as spoken transitions and simple explanations. Keep page language short; let the speaker notes carry the live explanation.

### The Redesign Still Looks Like A Normal Business Report

Symptoms:

- Every page is title + cards.
- The composition is evenly centered and low-risk.
- The palette is tuned, but the page has no visual metaphor.
- The source page structure is still visible under the redesign.
- There are no stage moments, oversized claims, evidence reveals, or strong focal points.

Fix:

1. Stop changing colors.
2. Rewrite the page role sequence.
3. Create a subject-specific visual metaphor.
4. Pick 3-5 recurring motifs.
5. Recompose the pages around focal scenes, not containers.
6. Keep original source pages as evidence, not as the main layout.

### The Reference Style Was Copied As A Palette Only

Fix: use the applicable confirmed visual source. For `reconstruct`, return to the confirmed VI board and compile its composition, hierarchy, motifs, source treatment, module language, evidence treatment, and preserve/avoid rules; never infer sequential behavior from the still image. For `corporate_fidelity`, load the compiled project shell unchanged: fixed screenshot crops stay stationary on every page, all report DOM and fragments stay inside the confirmed editable region, and the full screenshot never becomes a background. Presentation behavior comes from the confirmed use mode and runtime contract, not from the reference.

## 14. Minimal Delivery Template

When the user asks for a complete deck/report, produce:

- Final deck file.
- Asset folder.
- Speaker notes.
- Optional portable zip.
- Brief change summary.
- Verification summary.
- `《待核实内容清单》` with page/content, supplement type, source status, and suggested action.

When the user asks only for strategy, produce:

- Recommended story spine.
- Section-by-section page plan.
- Evidence needed.
- Design direction.
- Risks or open questions.
