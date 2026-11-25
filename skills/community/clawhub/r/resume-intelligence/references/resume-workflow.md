# Resume Workflow

## Compatibility Rule

Current resume-generation behavior remains the default. Helpers, schemas, and quality gates assist the agent-guided workflow but do not replace it. Do not block generation unless an output would expose credentials, secrets, private URLs, or unapproved confidential details.

## Source Inventory and Tool Log

Before writing `evidence.md`, create:

- `source-inventory.md`: all approved sources, folders, files, connector scopes, web searches, job postings, and scan status.
- `tool-usage-log.md`: the concrete tool, command, connector, browser, or manual input used for each source.

For local folders, recursively enumerate the full approved root. Prefer `rg --files <folder>` and record the command. Use `find` only as a fallback. The inventory must include nested files from every subfolder, not only the first folder discovered.

Classify each local file:

- Scanned: evidence extracted or inspected.
- Skipped unsupported format: file exists but no parser/tool is available.
- Skipped too large: file needs narrowing, conversion, or user approval.
- Skipped binary: binary file not useful for resume evidence.
- Skipped permission: access failed.
- Duplicate: same content or duplicate export already scanned.
- Needs user input: likely relevant, but requires context or conversion.

Do not write polished claims from sources that are not represented in the inventory and tool log.

## Optional Source Inventory Helper

For local evidence folders, the deterministic inventory helper can create a first-pass source coverage record:

```bash
python3 plugins/resume-intelligence/skills/resume-intelligence/scripts/inventory_sources.py <approved-folder> --output resume-runs/<run>/source-inventory.md
```

Use helper output as source coverage evidence, not as final resume claims. The agent still needs to extract, verify, deduplicate, and contextualize evidence before writing `evidence.md` or resume bullets.

## Evidence First

Start with `evidence.md`. Do not write polished resume bullets until the evidence log has source contexts, claims, confidence, and disclosure and quoting rules.

For each claim, capture:

- Claim text.
- Source context ID.
- Evidence reference.
- Confidence: high, medium, or low.
- Disclosure level: public, internal-summary-only, confidential, excluded, or unknown.
- Resume use: include, include-sanitized, needs-confirmation, or exclude.

## Bullet Quality

Strong bullets connect action, technical depth, scope, and impact:

```text
Led <action> for <system/product/domain>, using <technology/method>, improving <metric/outcome> across <scale/audience>.
```

When metrics are unavailable, use truthful scope:

```text
Designed <system/change> for <team/platform>, reducing operational risk and enabling <business or engineering outcome>.
```

Do not invent metrics. Ask the user for numbers when a bullet needs quantitative support.

## Resume Order

For a general technical resume:

1. Name and contact placeholders if the user has not provided them.
2. Professional summary.
3. Core skills.
4. Professional experience.
5. Selected projects or open-source contributions.
6. Education and certifications.

For a job-specific resume:

1. Align summary to the role and seniority.
2. Reorder skills to match the posting.
3. Select bullets with the strongest evidence for the posting's requirements.
4. Preserve truthfulness and disclosure and quoting rules.
5. Add a gap analysis instead of hiding missing requirements.

## Detailed Interview Resume

Create `detailed-resume.md` when the user asks for a detailed resume, master resume, full career timeline, interview preparation, or all work history with roles, responsibilities, impact, and metrics.

This file is intentionally more detailed than `professional-resume.md`. It is not the primary ATS submission file. Use it to help the user prepare for interviews, reconstruct career history, and select the strongest stories.

Include:

- Full career timeline with dates, company, title, team/product, scope, technologies, source evidence, and confidence.
- Role-by-role responsibilities and ownership.
- Key projects and workstreams under each role.
- For each project: problem, user role, architecture or technical approach, responsibilities, decisions, tradeoffs, technologies, collaborators, scale, impact, metrics, evidence, and interview story angle.
- Impact summary by reliability, performance, cost, security, scale, adoption, developer productivity, and business/customer outcome.
- Open-source and public work with dates, contribution type, role, impact, and evidence.
- Technical depth by period: expert, working knowledge, exposure, or gap.
- Metrics bank with value, context, source, confidence, and disclosure status.
- Interview story index for system design, technical deep dive, leadership, conflict, failure, and ambiguity.
- Missing-information questions for gaps that block a credible interview story or accurate timeline.

Ask the user for missing information instead of inventing it. Prioritize questions about dates, ownership, scope, metrics, sensitive details, and outcomes.

## Career Master Run And Coaching

Create `career-master-run.md` when the user wants a comprehensive career rebuild, coaching package, or full preparation system. Use it to connect evidence coverage, resume strategy, interview strategy, LinkedIn positioning, and job-search direction in one place.

Create `missing-information-loop.md` when dates, metrics, ownership, disclosure decisions, or scale are missing. Ask the highest-priority questions first and preserve unanswered questions for future sessions.

Create `career-positioning-coach.md` after `detailed-resume.md` and `resume-scorecard.md` when the user wants stronger positioning or when seniority/target-role alignment needs explanation. Keep the advice evidence-backed and practical: best-fit roles, seniority signals, differentiators, positioning risks, and next actions.

## Career Knowledge Vault

Create `career-vault/` when the user asks for future optimization, reusable career knowledge, Obsidian, an LLM wiki, or a persistent knowledge base of work history.

Use `references/career-vault-workflow.md` and build the vault from structured evidence, not raw unsupported claims. The vault should compile projects, technologies, disclosure decisions, and interview notes into Obsidian-friendly Markdown pages with source context references.

When `evidence.json` is available, run:

```bash
python3 plugins/resume-intelligence/skills/resume-intelligence/scripts/build_career_vault.py resume-runs/<run>/evidence.json --output-dir resume-runs/<run>/career-vault --run-name "<target role or run>" --run-date YYYY-MM-DD
python3 plugins/resume-intelligence/skills/resume-intelligence/scripts/vault_lint.py resume-runs/<run>/career-vault > resume-runs/<run>/career-vault-lint.md
```

If only Markdown evidence is available, create structured records first or build pages manually using the same fields: project, technologies, source context, evidence reference, confidence, disclosure level, and resume use.

## Job Posting Match

For each important job requirement, classify:

- Strong match: direct evidence exists.
- Partial match: adjacent evidence exists.
- Gap: no evidence found.
- Needs user input: likely experience but not supported by collected sources.

Use this classification in `gap-analysis.md`, then produce `targeted-resume.md` and `cover-letter.md`.

## Job Search and Match Scoring

When the user asks to search for matching jobs, use current public sources or user-approved job boards available through tools. Record the search date, query, location, remote preference, years of experience filter, and source URL in `source-inventory.md` and `tool-usage-log.md`.

Score each job in `job-match-report.md` using transparent criteria:

- Role and seniority fit: title family, level, years of experience, leadership expectations.
- Technical fit: required and preferred technologies supported by evidence.
- Domain fit: platform, cloud, AI, data, security, product, enterprise, open-source, or other target domains.
- Impact fit: scale, reliability, cost, migration, incident, adoption, or business outcomes.
- Location and work model fit.
- Evidence strength: direct, adjacent, weak, or unsupported.
- Gap risk: must-have gaps, missing certifications, missing domain experience, or unclear eligibility.

Use a 0-100 score or a qualitative strong/medium/low match, but show the reasoning. Do not recommend applying to a job solely because a keyword appears in the resume. When a listing is unavailable, expired, or inaccessible, mark it and do not score it as a live opportunity.

## Run Summary

Create `run-summary.md` for substantial runs, especially when multiple sources, connectors, generated artifacts, quality gates, or sensitive approval decisions are involved. It should show source coverage, tools used, outputs created, warning-only quality-gate findings, sensitive details that still need approval, and missing user questions that affect resume accuracy or disclosure.

## Resume Scorecard

Create `resume-scorecard.md` before final resume wording. Use it as a gate before producing `professional-resume.md`, `targeted-resume.md`, and `designed-resume.html`.

Quality gates are warning-only for normal resume generation. Record unsupported claims, missing evidence, ATS risks, page-length concerns, keyword gaps, and sensitive approval needs, but continue producing requested outputs unless proceeding would expose credentials, secrets, private URLs, or unapproved confidential details.

### Page-Length Strategy

- Recommend one page for early-career profiles, highly focused applications, or when the strongest evidence fits cleanly without shrinking text.
- Recommend two pages by default for senior, staff, principal, management, enterprise, or open-source-heavy profiles with more than about 8 years of experience.
- Recommend more than two pages only for academic CVs, federal/government resumes, patent/publication-heavy profiles, executive packets, or when the user explicitly asks.
- Never reduce readability to force one page. Prefer a clean two-page resume over tiny text, cramped margins, or deleted impact.

### ATS Safety

For the ATS-safe resume, check:

- No profile photo, icons, text boxes, complex tables, headers/footers carrying important content, or multi-column content that must parse correctly.
- Standard section headings: Summary, Technical Skills, Professional Experience, Selected Projects, Open Source, Education, Certifications.
- Text-based Markdown/DOCX/PDF source, not an image-only or scanned PDF.
- Plain job titles, company names, dates, skills, and bullets that an applicant tracking system can extract.
- No hidden keyword stuffing or unsupported claims.

The designed HTML resume can be more polished, but it is not the primary ATS submission format.

The DOCX application resume should follow the same ATS-safe rules. If a more impressive visual DOCX is requested, create it as a companion `designed-resume.docx`, not as the only application resume.

### Recruiter First-Page Strength

The first page should show the role match within a short skim:

- Header or summary includes the target role family and seniority.
- Summary states domain, scope, leadership level, and strongest technical themes.
- Skills are grouped by category and prioritize the target role's required technologies.
- The first experience section contains the strongest 3-5 quantified or scope-backed bullets.
- Enterprise work is sanitized without becoming vague.
- Public open-source contributions appear when they strengthen the target role match.

### Keyword Coverage

When a job posting is provided, extract keywords into:

- Role and seniority keywords.
- Required technologies.
- Preferred technologies.
- Domain and platform terms.
- Leadership and collaboration terms.
- Outcome terms such as reliability, cost, latency, scale, security, adoption, productivity, or incident reduction.

For each keyword, classify:

- Covered: direct evidence supports using the keyword.
- Partial: adjacent evidence supports a related keyword.
- Gap: no evidence supports it.
- Needs user input: likely experience but not supported by collected sources.
- Exclude: keyword would be misleading or unsupported.

Use exact posting terms naturally when evidence supports them. Do not add keywords only to game ATS ranking.

### Scorecard Outcome

End the scorecard with:

- Recommended page count.
- ATS risk level: low, medium, or high.
- Recruiter skim strength: strong, adequate, or weak.
- Keyword coverage percentage or qualitative summary.
- Top five fixes before applying.
- Claims that need user confirmation.

## Interview Preparation

When interview preparation is requested, derive preparation content from `evidence.md`, `professional-resume.md`, `resume-scorecard.md`, job postings, and job match findings.

Create `project-interview-briefs.md` for key projects. For each project include:

- One-line project positioning.
- 30-second and 90-second interview pitch.
- STAR story: situation, task, action, result.
- Architecture overview and major components.
- User ownership, decisions, tradeoffs, and conflicts resolved.
- Technologies used and why they mattered.
- Scale, reliability, performance, security, cost, migration, or operational impact.
- Metrics and honest metric gaps.
- Failure modes, lessons learned, and what the user would improve.
- Likely interviewer follow-up questions and concise answer notes.
- Sensitive details that must be anonymized.

Create `technical-stack-interview-guide.md` for important technologies. For each technology include:

- Where it appears in the user's evidence.
- Why the technology was used.
- Core concepts the user should be able to explain.
- Architecture role, tradeoffs, alternatives, and anti-patterns.
- Scaling, reliability, security, observability, deployment, and debugging angles.
- Interview questions with evidence-backed answer outlines.
- Hands-on or system-design topics to refresh.

Create `interview-prep-pack.md` as the practical study plan:

- Recruiter screen narrative.
- "Tell me about yourself" answer.
- Behavioral stories mapped to leadership, ambiguity, conflict, failure, influence, mentoring, and delivery.
- Technical deep dives and system design prompts.
- Coding or troubleshooting practice areas when relevant.
- Job-specific preparation from the target listing or job match report.
- Questions to ask interviewers.
- Red flags, gaps, and user follow-up questions.

Create `interview-readiness-scorecard.md` when the user asks for an interview coach or when a target job is selected. Score recruiter-screen narrative, resume walk-through, key project deep dives, technical stack explanations, system design preparation, behavioral stories, job-specific requirements, and redaction safety. Every weak score should include the next practice action and the evidence or user answer needed.

## Designed Resume

Create `designed-resume.html` when the user requests a professional template, visual resume, Canva/Figma-ready layout, printable design, PDF export, recruiter-facing design, or profile-picture support.

Use the sanitized content from `professional-resume.md`. Keep the Markdown resume as the ATS-friendly source of truth.

Create `ats-resume.docx` and `designed-resume.docx` when the user requests DOCX, Word, Google Docs, PDF export, or a more impressive resume template. Before creating DOCX files, read `docx-template-workflow.md`.

When the user wants the design to be impressive, read `visual-design-tools-workflow.md` and `visual-template-profiles.md`, create `visual-template-selector.md`, and prefer HTML/PDF/Figma for the visual artifact. DOCX can be polished, but it should not be treated as the highest-fidelity design surface.

The designed resume should:

- Use a restrained professional layout.
- Include a profile-picture slot only when the user provides or requests one.
- Use local image paths or clear replacement comments instead of fetching images.
- Include print CSS for browser-to-PDF export.
- Include a short comment explaining that the HTML can be copied into Canva, Figma, Google Docs, Word, or another design tool.
- Avoid decorative elements that make content hard to scan.
- Produce `visual-design-review.md` when browser, PDF, Figma, or Canva handoff is part of the request.
- Produce `visual-tool-handoff.md` when the user asks for Canva, Figma, another design tool, or manual design editing.

The designed DOCX should:

- Use a named template profile: `modern-technical` or `executive-compact`.
- Use normal Word document flow for core content.
- Render cleanly to page images before delivery when the Documents skill renderer is available.
- Be labeled as recruiter/referral-ready when it uses layout features that are not ideal for ATS parsing.

For Canva or Figma handoff:

- Do not upload private content automatically.
- Use sanitized copy blocks and local visual artifacts first.
- Use Figma MCP tools only when the user provides or approves a target Figma file.
- Keep `ats-resume.docx` as the job-portal submission file.

## LinkedIn Recommendations

Recommend editable changes for:

- Headline.
- About section.
- Experience sections.
- Featured projects or repositories.
- Skills ordering.
- Open-source positioning.
- Disclosure-safe enterprise project wording.

Do not post changes automatically. Keep suggestions in `linkedin-recommendations.md`.
