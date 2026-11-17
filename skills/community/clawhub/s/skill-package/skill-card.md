## Description:

Automated lead generation pipeline that finds local businesses with weak/no websites, AI-generates custom demo sites, deploys to Vercel, and runs a 5-email cold outreach drip sequence via AgentMail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[razzledazzlei](https://clawhub.ai/user/razzledazzlei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, sales operators, and automation builders use this skill to set up a local-business lead generation workflow that discovers prospects, queues them for approval, creates demo websites, deploys them, and sends outreach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run mutable external code while handling API credentials.

Mitigation: Use a pinned, reviewed source version in an isolated environment, then configure least-privilege API keys only after review.

Risk: Google service-account credentials and lead data may expose business or contact information if mishandled.

Mitigation: Protect service-account keys, restrict sheet access, and document how to delete lead records and generated-site data.

Risk: Automated public deployments can publish inaccurate or unwanted demo sites.

Mitigation: Require manual approval before public deployment and keep daily deployment limits enabled.

Risk: Scheduled cold email automation can send unwanted or excessive outreach.

Mitigation: Require approval before each email batch, use dry runs first, set strict sending limits, and document how to disable cron or systemd jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/razzledazzlei/skills/skill-package)
- [Google Sheet Setup](references/google-sheet-setup.md)
- [Environment Variables Reference](references/env-example.md)
- [5-Email Drip Sequence](references/drip-sequence.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration examples, and workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and operating guidance for a pipeline that may create JSON run artifacts, HTML demo sites, screenshots, QA reports, deployment metadata, and outreach email content.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
