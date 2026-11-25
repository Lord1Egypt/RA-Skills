---
name: resume-intelligence
description: Use when the user wants to build or tailor a resume, detailed interview resume, career master run, career coach, interview coach, career knowledge vault, Obsidian/LLM wiki, professional DOCX template, visual HTML/PDF resume, Canva-ready or Figma-ready resume, ATS/recruiter scorecard, cover letter, LinkedIn recommendations, interview prep, project interview briefs, technical-stack guide, job match scoring, redaction review, or career evidence summary from LinkedIn content, local project docs, Confluence, Jira, public GitHub, GitHub Enterprise, open-source work, profile pictures, or job postings. Trigger for resume drafting, tailoring, full career timeline, roles and responsibilities, impact metrics, ATS checks, keyword matching, DOCX generation, visual design tools, Canva/Figma handoff, browser/PDF rendering, project evidence extraction, recursive workspace analysis, durable career memory, tool auditing, job search, and interview prep.
---

# Resume Intelligence

Use this skill to convert approved career evidence into a professional resume and interview system: source inventory, tool usage log, evidence log, draft resume, detailed interview resume, career master run, career knowledge vault, career positioning coach, ATS/recruiter scorecard, polished resume, optional ATS-safe DOCX, optional designed HTML/PDF/Figma/Canva-ready resume, optional designed DOCX companion, optional targeted resume, optional cover letter, job/market fit analysis, job match scoring report, project interview briefs, technical-stack interview guide, interview readiness scorecard, interview prep pack, disclosure approval queue, redaction review, and LinkedIn profile recommendations.

## Guardrails

- Do not scrape LinkedIn behind login or bypass platform controls.
- Use LinkedIn profile exports, pasted profile content, public profile content, or user notes.
- Do not store credentials in plugin files, generated outputs, templates, or evidence logs.
- Do not upload profile pictures, private documents, or resume content to Canva, Figma, or another third-party design service automatically.
- Treat GitHub Enterprise, private Confluence, private Jira, and private repositories as confidential by default.
- Preserve source provenance for every claim.
- Mark uncertain claims for user confirmation.
- Ask before including internal project names, customer names, repository names, Jira IDs, Confluence titles, private URLs, or exact internal metrics in final user-facing outputs.
- Do not copy wording from other professionals' public profiles.

## When To Load References

- Read `references/source-model.md` before collecting evidence from more than one source or any GitHub source.
- Read `references/evidence-schema.md` before creating structured evidence, run summaries, or quality-gate checks.
- Read `references/privacy-sanitization.md` before writing final resume, cover letter, or LinkedIn text from enterprise or private sources.
- Read `references/enterprise-redaction-audit.md` before finalizing outputs from GitHub Enterprise, private Confluence, Jira, private repositories, or confidential local documents.
- Read `references/resume-workflow.md` before producing the evidence log, resume files, cover letter, or LinkedIn recommendations.
- Read `references/career-coaching-workflow.md` before producing career master runs, career positioning advice, interview coaching, readiness scoring, or missing-information loops.
- Read `references/career-vault-workflow.md` before creating or querying a durable Career Knowledge Vault, Obsidian vault, LLM wiki, or future-use career memory.
- Read `references/docx-template-workflow.md` before producing DOCX, Word, Google Docs-targeted, PDF-export, Canva-ready, Figma-ready, or visually polished resume artifacts.
- Read `references/visual-design-tools-workflow.md` before producing visually rich HTML/PDF output, Canva-ready packages, Figma handoff, browser-rendered screenshots, or deciding whether DOCX is the right final visual surface.
- Read `references/visual-template-profiles.md` before selecting a named visual resume profile or using a profile picture in a visual artifact.
- Read `references/interview-job-workflow.md` before producing project interview briefs, technical-stack interview guidance, interview preparation content, job search results, or job match scoring.
- Read `references/open-source-onboarding.md` and `references/prompt-library.md` when the user asks for setup help, local-only mode, open-source installation, or reusable prompts.

## Intake

Start by identifying the run goal:

- General resume.
- Detailed interview resume or master career timeline.
- Role-specific resume.
- Company-specific resume.
- Job-posting-specific resume and cover letter.
- LinkedIn profile recommendations.
- Career positioning or interview coaching.
- Career Knowledge Vault, Obsidian vault, LLM wiki, or future-use knowledge base.
- Professional DOCX, HTML/PDF, Figma-ready, Canva-ready, or visual template generation.
- Interview preparation from resume evidence.
- Job search and match scoring.
- Evidence extraction only.
- Safe local-only run or setup validation.

Collect only the inputs needed for that goal:

- Years of experience and target seniority.
- Target roles, technologies, domains, and geography.
- LinkedIn profile export, pasted profile, public profile content, or notes.
- Local project-document folder path.
- Confluence CQL queries, spaces, titles, or page URLs approved by the user.
- Jira JQL queries, projects, issue keys, assignee identity, and date ranges approved by the user.
- Public GitHub account, repositories, PRs, issues, and date ranges.
- GitHub Enterprise host, username, organization, repositories, credential context, contribution type, date range, and disclosure level.
- Job posting text, URL content, or pasted listing.
- Optional local profile-picture path or attachment for designed resume templates.
- Confidentiality and redaction preferences.
- Safe local-only mode preference and any third-party upload restrictions.

## Source Collection

Create a source context for each approved source. Keep public GitHub and GitHub Enterprise separate even when the same person owns both identities.

Always create `source-inventory.md` and `tool-usage-log.md` before `evidence.md`. The inventory must prove what was in scope, what was scanned, what was skipped, and why. The tool log must record the concrete tools, connector calls, shell commands, browser actions, or manual inputs used for each source. Do not silently infer that a folder or connector was read.

For local document folders, recursively enumerate the approved root with `rg --files <folder>` whenever available. Use a `find` fallback only when `rg` is unavailable or unsuitable. Do not stop after the first subfolder. Include every nested file in the inventory, then classify files as scanned, skipped-unsupported-format, skipped-too-large, skipped-binary, skipped-permission, duplicate, or needs-user-input. Prefer text-oriented formats such as `.md`, `.txt`, `.csv`, `.json`, `.yaml`, `.yml`, `.html`, `.xml`, `.adoc`, `.rst`, `.log`, `.docx`, and `.pdf` when local extraction tools are available; record extraction limitations for formats that cannot be parsed.

If connector tools are available, use them after the user approves the query or repository scope:

- GitHub: repositories, authored pull requests, reviewed pull requests, issues, commits, comments, and diffs when relevant.
- Confluence: user-approved CQL searches and specific pages.
- Jira: user-approved JQL searches and selected fields.
- Local files: inspect text-oriented documents under the approved folder.
- Web research: use current public sources for job postings and public market research when the user asks for optimization or targeting.
- Profile picture: use only a user-provided local image path or attachment, and include it only in designed artifacts when requested.

If a connector is unavailable, credentials are missing, or a scoped source cannot be accessed, record the attempt in `tool-usage-log.md`, mark the source context as unavailable or needs-user-input, ask for pasted exports, local files, or manual summaries, and continue with other approved sources.

## Evidence Extraction

For each source, extract:

- Project or product name.
- Source context and evidence reference.
- User role and ownership.
- Business, customer, technical, operational, security, or platform problem.
- Actions performed by the user.
- Technologies and platforms.
- Scale, reliability, performance, cost, adoption, security, migration, or operational impact.
- Dates or time windows.
- Quantitative metrics.
- Collaborators and cross-functional scope.
- Confidence level: high, medium, or low.
- Disclosure level: public, internal-summary-only, confidential, excluded, or unknown.

Prefer direct evidence over inference. When evidence conflicts, ask the user which version is accurate.

## Output Location

Create outputs under:

```text
resume-runs/YYYY-MM-DD-<descriptive-slug>/
```

Use these filenames when the corresponding output is requested:

- `source-inventory.md`
- `tool-usage-log.md`
- `evidence.md`
- `run-summary.md`
- `safe-local-mode-checklist.md`
- `disclosure-approval-queue.md`
- `final-redaction-review.md`
- `draft-resume.md`
- `detailed-resume.md`
- `career-master-run.md`
- `career-vault/`
- `career-vault-lint.md`
- `missing-information-loop.md`
- `career-positioning-coach.md`
- `resume-scorecard.md`
- `professional-resume.md`
- `ats-resume.docx`
- `designed-resume.docx`
- `designed-resume.html`
- `designed-resume.pdf`
- `visual-template-selector.md`
- `visual-design-review.md`
- `visual-tool-handoff.md`
- `targeted-resume.md`
- `cover-letter.md`
- `linkedin-recommendations.md`
- `gap-analysis.md`
- `job-match-report.md`
- `project-interview-briefs.md`
- `technical-stack-interview-guide.md`
- `interview-readiness-scorecard.md`
- `interview-prep-pack.md`
- `docx-render-review.md`

Use the templates in `assets/templates/` as structure, not as rigid wording.

## Output Sequence

1. Build `source-inventory.md` and `tool-usage-log.md` first.
2. If the user wants local-only mode, create `safe-local-mode-checklist.md` and avoid connector, browser, Figma, Canva, and job-board access unless the user later approves it.
3. Build `evidence.md` from scanned or manually provided sources only.
4. If private or enterprise sources are used, create `disclosure-approval-queue.md` before final user-facing wording.
5. Create `draft-resume.md` from high- and medium-confidence evidence.
6. If the user wants full interview preparation, career reconstruction, "all work timeline" detail, or career coaching, create `detailed-resume.md`, `career-master-run.md`, and `missing-information-loop.md` before the scorecard. Include full work chronology, roles, responsibilities, project ownership, impact, metrics, technologies, leadership scope, and questions for missing information.
7. If the user wants future optimization, durable knowledge, Obsidian, an LLM wiki, or reusable career memory, create or update `career-vault/` from structured evidence, then run `scripts/vault_lint.py` and save the result as `career-vault-lint.md`.
8. Ask the user to confirm low-confidence claims and sensitive details before final wording.
9. Create `resume-scorecard.md` before final wording. Check page-length strategy, ATS parse safety, first-page recruiter strength, keyword coverage, unsupported claims, and job-posting gaps.
10. If career positioning is requested or useful for a senior/profile rewrite, create `career-positioning-coach.md` from the detailed resume and scorecard.
11. Create `professional-resume.md` using sanitized, evidence-backed bullets and the scorecard recommendations.
12. If DOCX, Word, or Google Docs is requested, create `ats-resume.docx` as the primary application version and optionally `designed-resume.docx` for recruiter/referral sharing. Use `scripts/build_resume_docx.py` when it fits the content, then render-check the DOCX with the Documents skill before delivery.
13. If an impressive visual resume, recruiter-facing resume, Canva/Figma-ready layout, profile picture, or PDF export is requested, create `visual-template-selector.md`, make `designed-resume.html` the primary visual artifact, render it with browser tooling when available, and create `designed-resume.pdf`, `visual-design-review.md`, and `visual-tool-handoff.md` when requested or useful. Use Figma tools only when the user provides or approves a Figma target file; use Canva only as a manual/import handoff unless the user explicitly approves uploading sanitized content.
14. If a job posting is provided, create `gap-analysis.md`, `targeted-resume.md`, and `cover-letter.md`.
15. If job search is requested, search current public job sources and create `job-match-report.md` with match scoring and citations.
16. If interview preparation is requested, create `project-interview-briefs.md`, `technical-stack-interview-guide.md`, `interview-prep-pack.md`, and `interview-readiness-scorecard.md`.
17. Create `linkedin-recommendations.md` with editable profile updates.
18. If private or enterprise sources informed final outputs, create `final-redaction-review.md` before delivery.
19. Create `run-summary.md` for substantial runs summarizing source coverage, tools used, outputs created, warning-only quality gates, sensitive approval needs, career vault status, and missing user questions.

## Final Response

Summarize:

- Files created.
- Sources used and skipped.
- Inventory and tool-log coverage, including any approved folders or connector scopes that were unavailable.
- Sensitive items that require user review.
- Low-confidence claims that need confirmation.
- Detailed resume gaps: missing dates, responsibilities, metrics, scope, project outcomes, or stories that require user input.
- Career positioning and interview readiness gaps when coaching outputs were requested.
- Career vault path, lint status, and any missing evidence links when durable knowledge was requested.
- Scorecard findings for ATS safety, recruiter strength, page length, and keyword gaps.
- Visual tool path used: HTML/PDF, Figma, Canva handoff, DOCX, or multiple outputs.
- Visual template profile and profile-picture approval status when visual outputs were requested.
- Disclosure approval and final redaction status when private sources were used.
- DOCX template used, render-check status, and whether the delivered DOCX is ATS-safe, designed, or both.
- Strongest job matches and interview preparation gaps when those outputs were requested.
- Clear next actions for the user.
