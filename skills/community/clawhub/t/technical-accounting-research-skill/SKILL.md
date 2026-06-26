---
name: technical-accounting-research
description: Research technical accounting treatment and financial statement disclosure for specific transactions using U.S. GAAP and SEC-focused sources. Use when a user asks how to account for a transaction, what journal entries, presentation, or disclosures are required, or needs accounting-position documentation in memo, email, or Q-and-A DOCX format.
---

# Technical Accounting Research

## Overview

Handle transaction-specific accounting questions through a fixed sequence: gather facts, confirm output format, ensure the local FinResearchClaw repo is installed and runnable, route the task through that wrapped repo/workflow, research guidance online, apply standards, and deliver the requested output.

For all tasks under this skill — memo, email, and q-and-a alike — the workflow must wrap and leverage the local FinResearchClaw repo/workflow as a required research-and-drafting execution layer. This is mandatory, not optional, and applies even when the accounting issue appears straightforward. The skill may create and use a task-local virtual environment when needed to run the repo or supporting document-generation dependencies. FinResearchClaw is a required support engine for research depth and drafting quality across all output modes; authoritative accounting conclusions must still be grounded in ASC / SEC / AICPA / clearly labeled interpretive guidance.

## Prerequisites

Before using this skill for substantive completion, install and make available the local FinResearchClaw repo:

1. Clone or install `https://github.com/ChipmunkRPA/FinResearchClaw`
2. Ensure the local repo is available at `~/.openclaw/workspace/AutoResearchClaw` unless a different local path is intentionally configured
3. Ensure Python is available and create a task-local virtual environment when needed
4. Install memo-generation dependencies such as `python-docx` when DOCX output is required

If FinResearchClaw is not installed locally and runnable, do not treat the full research workflow as ready. Fix that prerequisite first.

## Required Behavior

- Ask clarification questions before analysis.
- Confirm requested output format: `memo`, `email`, or `q-and-a`.
- If the user asks for a `memo`, default the deliverable to a `.docx` file saved in the user's `~/Downloads` folder unless the user explicitly requests a different location or format.
- For `memo` requests, do not post the full memo body directly into chat by default. Instead, generate the DOCX deliverable and reply with a short status note that the file was created and where it was saved.
- The final memo DOCX must be client-ready and must not expose Markdown syntax (for example `#`, `##`, `###`, `####`, bullet markers used as raw source notation, or fenced code blocks) anywhere in the rendered document.
- **Avoid bullet points** in the final memo; use separate, meaningful, and structured narrative paragraphs for all sections.
- **Avoid numbered sections**; use proper professional formatting for section headings without prepended numbers.
- The memo and any delivered document must use **Times New Roman, 12pt, black font**.
- **Avoid Markdown symbols** like `***` or `**` (for bold) if they might be rendered literally; use native DOCX formatting.
- **Mandatory Real-Life Example**: Always perform a web search to find and include a real-world accounting example (public SEC filings preferred) or a secondary reference material example to demonstrate the practical application of the accounting treatment.
- Research the internet before final conclusions, even if guidance seems familiar.
- For all requests under this skill, use FinResearchClaw as a required wrapped execution and drafting layer.
- Do not present, summarize, or imply a substantive accounting conclusion to the user before the required FinResearchClaw-backed flow has been run, except to restate assumptions, ask clarifying questions, or explain that the analysis is still in progress.
- The skill may create and activate a task-local virtual environment to run FinResearchClaw, supporting scripts, and output-generation dependencies.
- Distinguish authoritative guidance from interpretive guidance.
- Cite sources with links and accessed date in the deliverable.
- Include at least **5 authoritative references** supporting the accounting conclusion unless fewer are genuinely available for the issue; if fewer than 5 authoritative references can be identified, disclose that constraint explicitly and supplement with clearly labeled interpretive guidance.
- If the user does not provide a company name for a memo or memo-style deliverable, default to the neutral defined party name **"Company"** throughout the document. Do not substitute other role labels such as "vendor," "customer," or similar labels as the primary unnamed entity reference unless the fact pattern itself requires naming multiple counterparties distinctly.
- State assumptions explicitly when facts remain unknown.
- Do not let FinResearchClaw-style output replace authoritative accounting analysis; use it to strengthen organization and completeness, not to dilute source hierarchy.

## Workflow

### 1. Intake and Scope

- Capture the user issue in one sentence.
- Confirm reporting basis and jurisdiction (`US GAAP`, `SEC filer status`, and whether disclosures are public-company or private-company focused).
- Confirm reporting period and materiality context.

### 2. Clarification Questions (Mandatory)

- Use [references/clarification-question-bank.md](references/clarification-question-bank.md).
- Ask only the questions needed for the fact pattern; do not skip critical facts.
- Pause analysis until enough facts are available to form a defensible conclusion.
- If facts stay incomplete, proceed with explicit assumptions and sensitivity notes.

### 3. Output Format Confirmation (Mandatory)

- Ask which format is required (`memo` for formal documentation, `email` for concise communication, `q-and-a` for direct question and answer support).
- If no preference is provided, default to `memo`.
- For `memo` outputs, default to generating a `.docx` file in `~/Downloads`.
- Unless the user explicitly asks to see the full memo inline, do not paste the memo text into the channel; provide the saved file path instead.

### 4. Research Guidance

- Research sources using the priority and reliability rules in [references/source-priority.md](references/source-priority.md).
- Prefer primary and authoritative sources first (FASB/SEC/AICPA standard-setting materials).
- Use Big 4 publications as interpretive support, not sole authority.
- For a memo conclusion, target at least **5 authoritative references** across the conclusion, disclosure direction, and key technical positions wherever the issue reasonably permits.
- Invoke FinResearchClaw for every task handled by this skill, regardless of output format.
- Execution for memo, email, and q-and-a outputs should all wrap the FinResearchClaw repo/workflow even if the accounting issue is straightforward.
- The FinResearchClaw-backed run must occur before any user-facing technical conclusion is given. Do not short-circuit from clarified facts directly to an accounting answer.
- The skill may create a task-local virtual environment for the run if needed.
- Do not skip or bypass the FinResearchClaw path. If the repo is unavailable, dependencies are missing, or the workflow fails to run, stop and troubleshoot the FinResearchClaw environment first. The task should not proceed to substantive completion until the wrapped FinResearchClaw path is functioning.
- Do not surface an accounting conclusion before this stage is completed successfully.
- At the start of a live task, explicitly verify that FinResearchClaw is installed locally and that the configured repo path exists before relying on the wrapped workflow.
- If using FinResearchClaw, treat it as a research accelerator and drafting assistant only; independently verify accounting conclusions against authoritative and clearly labeled interpretive sources before finalizing.
- Capture citation labels and URLs for each source used.

### 5. Technical Analysis and Illustration

- Frame the accounting issue.
- Map facts to recognition, measurement, presentation, and disclosure guidance.
- **Real-Life Illustration (Mandatory)**: Find and include a descriptive summary of a real-world case (e.g., an SEC filer's 10-K/Q disclosure) that mirrors the fact pattern. Explain how they applied the standard.
- Evaluate reasonable alternatives and explain rejection rationale.
- Conclude with recommended accounting treatment, disclosure direction, and key risks.
- Include journal entry examples when useful for implementation.
- For formal memo output, produce a polished memorandum style with a complete professional header and well-formed section headings (no numbers).
- If no company name is specified by the user, define the reporting entity as **"Company"** and use that term consistently throughout the memo.
- Analysis and all other sections must use descriptive, narrative paragraphs instead of bullet points or numbered lists.
- When FinResearchClaw is available, use it to improve thoroughness and professional drafting quality while preserving accounting-source hierarchy.
- Do not allow raw JSON structures, Python dictionary renderings, placeholder header fields, unformatted source dumps, or visible Markdown markers to appear in the final memo.
- If a drafting pass begins in Markdown, the final DOCX generation step must fully convert that draft into native memorandum formatting rather than packaging the Markdown text as-is.
- Preferred execution order for all outputs under this skill: (1) authoritative accounting research and fact development first, (2) create/use a task-local virtual environment if needed, (3) run the FinResearchClaw repo/workflow as the required drafting/research wrapper, (4) final manual verification against ASC/SEC/AICPA and labeled interpretive guidance, and (5) generate the requested deliverable format.

### 6. Draft and Materialize DOCX

- Build a JSON payload using [references/report-json-schema.md](references/report-json-schema.md).
- For `memo` requests, save the output DOCX to `~/Downloads` by default (for example, `~/Downloads/<descriptive-file-name>.docx`).
- Standard wrapped workflow for all outputs:
  1. gather facts and clarifications;
  2. perform authoritative and interpretive accounting research;
  3. create/use a task-local virtual environment if needed for the run;
  4. run the FinResearchClaw-supported drafting pass for every task under this skill;
  5. during memo-mode execution, send a short in-progress status update to the user at least every 1 minute until the memo workflow finishes or fails; each update should briefly state the current stage (for example fact gathering, authoritative research, FinResearchClaw run, memo drafting, citation verification, or DOCX generation);
  6. manually validate the final analysis, formatting, section structure, entity naming consistency, and citations;
  7. generate the requested deliverable format (DOCX for memo by default, or the requested email/q-and-a output) using a conversion path that renders headings, paragraphs, bullets, and tables as native document elements rather than leaving Markdown markers visible;
  8. review the finished output for presentation quality before responding;
  9. reply in chat with the appropriate completion note for the chosen format.
- Do not use a Markdown-to-DOCX path that can preserve raw Markdown notation in the final document. If the chosen conversion method leaves visible Markdown markers, treat that as a failed output and regenerate the memo with a native DOCX creation path.
- **Do not pass Markdown syntax through as final DOCX prose.** Convert section labels into schema fields and provide plain text content for paragraphs, bullets, and conclusions. The generated Word document must use native Word headings/lists rather than visible Markdown markers such as `#`, `##`, `###`, or `####`.
- Run:

```bash
python scripts/build_accounting_report_docx.py \
  --input-json <analysis.json> \
  --output-docx ~/Downloads/<technical-accounting-report>.docx \
  --format <memo|email|q-and-a>
```

- The script produces a DOCX with:
- Title and metadata.
- Facts and issue statement.
- Guidance table with links.
- Analysis and conclusion.
- Disclosure considerations.
- Open items and assumptions.

### 7. Quality Check

- Confirm the conclusion is consistent with cited guidance.
- Confirm all significant assumptions are disclosed.
- Confirm the output format matches user request.
- Confirm every external source in the analysis has a URL listed in the report.
- Confirm the final memo reads like a professional memorandum rather than a raw data export.
- Confirm headers are fully populated (for example To / From / Date / Subject) and that analysis sections render as proper prose, not serialized objects.
- Confirm the memo uses **"Company"** consistently when no specific company name was provided.
- Confirm the conclusion is supported by at least **5 authoritative references**, or that any shortfall is explicitly disclosed and justified.
- Confirm the rendered DOCX contains no visible Markdown syntax such as heading hashes, fenced code blocks, or raw list notation.
- No task under this skill may close without using the wrapped FinResearchClaw path successfully. If FinResearchClaw is not yet working, the required next step is to fix that environment rather than continue without it.

## Resources

- Clarifying question checklist: [references/clarification-question-bank.md](references/clarification-question-bank.md)
- Source hierarchy and citation rules: [references/source-priority.md](references/source-priority.md)
- JSON format for DOCX generation: [references/report-json-schema.md](references/report-json-schema.md)
- Example report payload: [references/example_report_input.json](references/example_report_input.json)
- DOCX generator: `scripts/build_accounting_report_docx.py`
- FinResearchClaw repo: `https://github.com/ChipmunkRPA/FinResearchClaw`
- FinResearchClaw local skill reference: `~/.openclaw/skills/finresearchclaw/SKILL.md`

## Dependency

Install once if needed:

```bash
python -m pip install --user python-docx
```

## Runtime / Environment Expectations

- Memo-mode runs are allowed to create and use a task-local Python virtual environment.
- FinResearchClaw default repo path: `~/.openclaw/workspace/AutoResearchClaw`
- If the repo or its dependencies are not ready, initialize a local venv for the task and install only the dependencies needed for the memo workflow.
- If FinResearchClaw cannot be executed after reasonable setup attempts, disclose that explicitly and fall back to a non-FinResearchClaw path only as an exception, not the default.
