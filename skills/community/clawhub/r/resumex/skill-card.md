## Description:

Auto Job Applying Agent helps users manage Resumex resumes, search for matching jobs, apply to selected job postings, log application outcomes, and optionally deliver resume summaries by Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atharva-badgujar](https://clawhub.ai/user/atharva-badgujar)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to manage resume data in Resumex and coordinate job search, job application, and job-tracker workflows through an agent. It is most relevant for candidates who want guided resume editing plus assisted application submission with explicit review of target jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit personal resume and contact data to job sites that may not be validated by the server evidence.

Mitigation: Keep AUTO_APPLY_MODE=false, review each ranked job URL before applying, avoid unfamiliar or generic application sites, and use manual application mode when confidence is low.

Risk: Resume and job-tracker workflows depend on a Resumex API key and optional Telegram credentials.

Mitigation: Use a dedicated revocable Resumex API key, avoid Telegram delivery unless needed, and keep credential values out of shared logs or transcripts.

Risk: Playwright browser automation and browser installation can weaken local isolation and may be blocked by job portals.

Mitigation: Install dependencies in a virtual environment or sandbox, keep the browser transparent without stealth tooling, and fall back to manual application when portals require CAPTCHA, MFA, PDF upload, or complex forms.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/atharva-badgujar/skills/resumex)
- [Publisher profile](https://clawhub.ai/user/atharva-badgujar)
- [Resumex](https://resumex.dev)
- [Resumex API documentation](https://resumex.dev/api-docs)
- [README](artifact/README.md)
- [Privacy policy](artifact/PRIVACY.md)
- [Security guide](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands, configuration values, links, and JSON status summaries from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ranked job lists, resume summaries, application status results, manual-apply instructions, API request examples, and setup guidance.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
