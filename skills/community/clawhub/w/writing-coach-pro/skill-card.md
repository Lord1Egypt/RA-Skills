## Description:

Analyzes writing for grammar, style, tone, readability, and consistency while learning user preferences to improve feedback over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, and agent users use this skill to review, rewrite, and coach prose across emails, reports, blog posts, resumes, and long-form documents. It produces grammar and style findings, readability metrics, rewritten text, and progress-oriented feedback based on a persistent writing profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Writing-derived history, issue descriptions, profile changes, session summaries, and excerpts may be stored locally or synchronized to a dashboard.

Mitigation: Review the storage behavior before processing confidential writing, protect the local data directory, and disable dashboard synchronization unless the user intentionally wants those records written to the dashboard backend.

Risk: The artifact claims it does not transmit or track data while its configuration enables dashboard synchronization after each session.

Mitigation: Treat the published security guidance as requiring review before installation and confirm the dashboard configuration before using the skill with sensitive content.

Risk: Submitted text is processed by the user's configured LLM backend, which may be cloud-hosted.

Mitigation: Use a local model for documents that must stay on the user's machine, or review the chosen LLM provider's data handling policy before submitting sensitive material.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/nollio/skills/writing-coach-pro)
- [Publisher profile](https://clawhub.ai/user/nollio)
- [Setup guide](SETUP-PROMPT.md)
- [Security notes](SECURITY.md)
- [Dashboard integration spec](dashboard-kit/DASHBOARD-SPEC.md)
- [NormieClaw terms site](https://normieclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports and inline text feedback, with optional shell command guidance and generated configuration or report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce quick reviews, full analysis reports, rewrites, coaching explanations, style profiles, progress reports, and dashboard-oriented writing metrics.]

## Skill Version(s):

1.0.0 (source: server release metadata and dashboard manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
