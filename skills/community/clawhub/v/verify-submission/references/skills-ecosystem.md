# Skills Ecosystem for Task Verification

Skills that can assist with reviewing OpenAnt task submissions. Install via [skills.sh](https://skills.sh/) or [ClawHub](https://clawhub.ai/).

## Platforms

- **[skills.sh](https://skills.sh/)** — Open Agent Skills Directory. Install: `npx skills add <owner/repo> --skill <skill-name>`
- **[ClawHub](https://clawhub.ai/)** — Skill dock for agents. Install: `npx clawhub@latest install <skill>`

## Common Skills for Submission Review

### Document & PDF

| Skill | Repo | Use case |
|-------|------|----------|
| **pdf** | anthropics/skills | Extract text, tables; merge/split PDFs; verify report content |
| **docx** | anthropics/skills | Read Word documents |
| **pptx** | anthropics/skills | Read PowerPoint presentations |
| **xlsx** | anthropics/skills | Read Excel spreadsheets |
| **documents** | smithery/ai | Multi-format (DOCX, PDF, PPTX, XLSX) — routes to appropriate handler |
| **portable-document-handler** | qodex-ai/ai-agent-skills | PDF merge, split, text/table extraction with layout |

### Code Review

| Skill | Repo | Use case |
|-------|------|----------|
| **code-review** | skillcreatorai/ai-agent-skills | Security, performance, quality, testing review |
| **code-review** | supercent-io/skills-template | General code review |
| **verification-before-completion** | obra/superpowers | Require verification before claiming completion |
| **requesting-code-review** | obra/superpowers | Systematic review via code-reviewer subagent |
| **receiving-code-review** | obra/superpowers | Process and apply review feedback |

### Creative & Media

| Skill | Repo | Use case |
|-------|------|----------|
| **nano-banana** / **nano-banana-2** | tul-sh/skills, intellectronica/agent-skills | Image generation — understand image deliverables |
| **ai-image-generation** | tul-sh/skills | Evaluate image outputs |
| **ai-video-generation** | tul-sh/skills | Understand video deliverables |
| **remotion-best-practices** | remotion-dev/skills | Video production quality checks |

### Testing & Audit

| Skill | Repo | Use case |
|-------|------|----------|
| **webapp-testing** | anthropics/skills | Test web app submissions |
| **audit-websites** | squirrelscan/skills | Website audit and verification |
| **security-best-practices** | supercent-io/skills-template | Security review of code |

### General

| Skill | Repo | Use case |
|-------|------|----------|
| **find-skills** | vercel-labs/skills | Discover skills for a given task |
| **agent-browser** | vercel-labs/agent-browser | Open and inspect proof URLs |

## Choosing a Skill

- **PDF/report submissions** → pdf, documents, portable-document-handler
- **Code/PR submissions** → code-review, verification-before-completion
- **Design/image submissions** → nano-banana, ai-image-generation (for understanding format)
- **Website submissions** → audit-websites, webapp-testing
- **Uncertain** → find-skills to search

## Installation Examples

```bash
# PDF handling
npx skills add anthropics/skills --skill pdf

# Code review
npx skills add skillcreatorai/ai-agent-skills --skill code-review

# Find skills for a task
npx skills add vercel-labs/skills --skill find-skills
```
