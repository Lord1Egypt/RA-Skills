---
name: user-guide-automation
description: Reusable workflow for generating formal, detailed Markdown user guides from web applications using browser exploration or user-provided flows. Uses screenshots for every step and keeps the structure DOCX-ready.
version: 1.0.0
metadata:
  hermes:
    tags: [web, user-guide, documentation, docx, browser, screenshots, automation]
    related_skills: [dogfood, ocr-and-documents, powerpoint]
---

# User Guide Automation for Web Applications

Use this skill when the user wants to create a formal, detailed user guide from a web application, especially when the output must be a Markdown document ready for later DOCX conversion.

## Core idea

This workflow is based on browser exploration, not source-code inspection.
The guide is built from what the web app shows in a live browser session:
- page structure from `browser_snapshot()`
- visual confirmation from `browser_vision()`
- interactions with `browser_click()`, `browser_type()`, `browser_scroll()`, and `browser_press()`
- console checks from `browser_console()` when needed

If the user provides a flow, follow that flow exactly.
If the user does not provide a flow, explore the web app and infer the main user journey.

This skill currently supports one output mode:
1. **Sprint-1 / draft mode** — output Markdown only, but structure it like a final document so it can be converted to DOCX later without re-authoring.

When a reference document is provided (for example a PDF user guide), extract its structural pattern first and turn it into a reusable Markdown blueprint before writing the actual guide. Preserve:
- front matter / cover pattern
- table of contents pattern
- section lettering or numbering style
- repeated subflow pattern (e.g. daftar/tambah/detail/edit/upload/hapus/arsip)
- screenshot placement rhythm
- instructional wording style

The default file naming convention is:
- `guide.md` for the main document
- `screenshots/` for evidence assets
- one nested folder per feature or workflow stage inside `screenshots/`


## Default requirements

- Output format: Markdown (.md) only
- Style: formal
- Detail level: detailed
- Screenshots: capture every step, not only important steps
- Audience: admin, regular user, or mixed depending on the web app
- Template: use the provided structure as a Markdown blueprint; do not generate DOCX in this skill


## Slash-command intake form

When the user runs `/user-guide-automation`, ask for the minimum required information in a copy-ready format:

- URL:
- Lokasi output:
- Scope: full site / fitur tertentu (sebutkan fiturnya)

Optional but recommended:
- Role:
- Credential:
- Flow:
- Template path:
- Output filename:
- Catatan khusus:

Rules:
- If the user chooses a specific feature scope, stay within that feature unless related navigation is needed.
- If the user chooses full site, explore the main journeys and major feature groups.
- If credentials are provided, use them only for the requested app and flow.

## Recommended workflow

### 1) Intake
Collect or confirm:
- target web app URL
- target user role, if relevant
- user-provided flow, if any
- DOCX template path
- output filename or folder
- whether the guide should cover one feature or the whole workflow
- screenshot output directory behavior (default: create `screenshots/` inside the output folder)

If the user did not provide a flow, proceed with exploration.

When the user provides only a top-level output folder, create this structure:
```
{output_dir}/
├── guide.md
├── screenshots/
│   ├── dashboard/
│   ├── ai-characters/
│   └── ...
└── references/
```
Use one subfolder per feature, page group, or workflow stage so screenshots stay organized. Use lowercase kebab-case folder names when possible.

### 2) Explore the web app
Open the app and identify the real user journey.
Use the browser tools in this order whenever useful:
- `browser_navigate(url=...)`
- `browser_snapshot()`
- `browser_vision(question=..., annotate=true)`
- `browser_click(ref=...)`
- `browser_type(ref=..., text=...)`
- `browser_scroll(direction=...)`
- `browser_press(key=...)`
- `browser_console(clear=true)` after navigation or significant interaction

For pages with animations, lazy loading, or scroll-revealed content, do not judge a section from one viewport alone. Scroll in small increments, pause briefly, then re-check with `browser_snapshot()` and/or `browser_vision()` before deciding content is missing or empty.

During exploration, collect only the UI details needed for the guide:
- page title
- menu names
- button labels
- field labels
- success/error messages
- breadcrumb/path names

Do not over-extract text. Keep it lean.

### 3) Build the step list
Create a step list that matches the real interaction sequence.
If a user flow exists, preserve the provided order.
If not, infer a practical order from the app UI.

Each step should include:
- step number
- action verb
- target UI element or page
- short explanatory note if needed
- screenshot reference

For sprint-1 Markdown drafts, organize the step list into document-like sections first, then steps. Use the same top-level section order that a DOCX template would later expect, so the MD stays conversion-friendly.

### 4) Capture screenshots for every step
Take screenshots for all steps, including intermediate ones.
Use screenshots as instruction illustrations, not as bug evidence.

If a step changes the page state, capture the new state immediately.

Practical lesson: when the workflow includes login, capture a dedicated login screenshot before entering the protected area. Do not reuse a later dashboard screenshot as evidence for the login step; keep the login step, post-login dashboard, and feature page as separate screenshots so the guide stays clear and accurate.

### 5) Write the guide text
Write formal Indonesian.
Preferred structure:
- title/cover
- table of contents if the template supports it
- section headings
- numbered steps
- concise but detailed instructions
- screenshot captions
- notes or warnings only when needed

Keep wording instructional and neutral.
Avoid QA language such as severity, issue, or defect.

### 6) Write the Markdown guide
If a template or blueprint is provided:
- reuse the existing Markdown structure
- preserve header/footer-equivalent sections only as text blocks
- keep the hierarchy consistent
- do not switch the output to DOCX in this skill

If the structure is blank:
- populate it cleanly with the generated guide content

### 7) Verify the final Markdown
Check that:
- all steps are present
- screenshots match the correct steps
- the language is formal
- the Markdown structure is complete and readable
- the output filename is correct

## When to use user-provided flow vs exploration

Use the user’s flow when:
- the user already knows the exact process
- the app is sensitive or complex
- the workflow must match a SOP exactly

Use exploration when:
- the user does not know the exact steps
- the app is unfamiliar
- the user wants the guide to be discovered from the live UI

## Token-saving rules

- Do not read or restate entire pages unless necessary
- Prefer `browser_snapshot()` for structure and refs
- Prefer `browser_vision()` only when layout or visuals matter
- Reuse a stable guide template
- Keep captions short
- Avoid repetitive descriptions across steps

## Important distinctions from dogfood

Dogfood is QA-oriented and looks for bugs.
This skill is documentation-oriented and looks for user actions.

Shared pieces borrowed from dogfood:
- browser exploration
- screenshots per step
- console checks when useful
- systematic flow execution

Differences from dogfood:
- no severity classification
- no bug reporting
- no reproduction section
- output is a user guide, not a QA report

## Suggested output pattern

- If the user gives a template path, treat it as a Markdown blueprint reference rather than a DOCX target
- If the user gives a duplicateable blank template, copy its structure into Markdown first
- Save the final document as `.md`
- Optionally save screenshot assets alongside it if needed for review


### Markdown blueprint mode
When the user wants a DOCX-like structure in Markdown first:
- start with the same cover/TOC/header order the final document will use
- keep section numbering stable
- preserve repeated subsection patterns across modules
- use short placeholder captions for screenshots
- keep the document ready for later DOCX conversion without changing the content hierarchy

## Practical checklist

Before finishing, confirm:
- [ ] The guide follows the right flow
- [ ] Every step has a screenshot
- [ ] The writing is formal
- [ ] The template formatting is preserved
- [ ] The Markdown file is complete and usable
