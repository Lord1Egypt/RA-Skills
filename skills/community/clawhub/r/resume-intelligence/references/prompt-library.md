# Prompt Library

These prompts are safe starting points for Codex, Claude, Cursor, or another local agent. Replace placeholders with approved sources only.

## Local-Only Career Master Run

```text
Use $resume-intelligence in safe local-only mode.
Approved sources:
- LinkedIn export or pasted profile: <path or pasted text>
- Local project documents: <folder>
- Local Git or project notes: <folder>

Target role: <role family>
Seniority and years of experience: <level and years>
Create source inventory, tool usage log, evidence log, detailed interview resume, ATS resume, visual HTML/PDF resume, career positioning coach, interview readiness scorecard, LinkedIn recommendations, and run summary.
Do not connect to external tools or upload content. Ask me before using internal names, customer names, repository names, exact private metrics, or profile pictures.
```

## Enterprise Evidence Run

```text
Use $resume-intelligence with separate source contexts for public GitHub, GitHub Enterprise, Jira, Confluence, and local documents.
Approved enterprise scope:
- GitHub Enterprise host and repositories: <host and repos>
- Jira JQL: <query>
- Confluence CQL or pages: <query or URLs>
- Disclosure default: internal-summary-only

Create disclosure-approval-queue.md and final-redaction-review.md before final outputs.
Do not include private URLs, issue keys, customer names, private repository names, or exact metrics unless I approve them.
```

## Job-Specific Application

```text
Use $resume-intelligence to tailor my resume and cover letter for this job posting: <posting URL or pasted text>.
Use my existing evidence folder: <resume-runs folder or evidence files>.
Consider years of experience, target seniority, required technologies, preferred technologies, and location/work model.
Create gap-analysis.md, targeted-resume.md, cover-letter.md, resume-scorecard.md, interview-prep-pack.md, and run-summary.md.
Do not add unsupported keywords. Put missing requirements in the gap analysis.
```

## Visual Resume And Canva/Figma Handoff

```text
Use $resume-intelligence to create an ATS-safe DOCX plus a recruiter-facing visual resume.
Visual template preference: <modern-technical | executive-compact | open-source-builder | enterprise-platform | ai-automation>
Profile picture: <local path or omit>
Create designed-resume.html, optional designed-resume.pdf, visual-template-selector.md, visual-design-review.md, and visual-tool-handoff.md.
Do not upload content to Canva, Figma, or another third-party tool without asking me first.
```

## Interview Coach

```text
Use $resume-intelligence as my interview coach for <target role or company>.
Use evidence from <resume-runs folder>.
Create project-interview-briefs.md, technical-stack-interview-guide.md, interview-prep-pack.md, interview-readiness-scorecard.md, and missing-information-loop.md.
Focus on architecture, tradeoffs, scale, reliability, security, operational ownership, leadership, conflict, failure, and measurable impact.
Ask concise questions for missing dates, ownership, metrics, scale, and sensitive details.
```
