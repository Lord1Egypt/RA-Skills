## Description:

Skill-D Create Issues coordinates an event-driven workflow that validates confirmed meeting issue drafts, creates Gitea issues with dependencies, updates meeting status, and prepares notification email payloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myd2002](https://clawhub.ai/user/myd2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and meeting workflow operators use this skill to turn confirmed meeting action items into tracked Gitea issues and follow-up notifications. It supports both webhook-triggered and chat-triggered confirmation flows for single-project and cross-project meetings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Insecure defaults may expose tokens or allow forged webhook events.

Mitigation: Use only an HTTPS Gitea endpoint, require a strong webhook secret, restrict token scope, protect the .env file, and avoid exposing the webhook listener publicly.

Risk: Setup and dependency installation can run in an unsafe environment if used with untrusted configuration.

Mitigation: Review setup.sh and .env before running, prefer a virtual environment, and pin or review dependencies before installation.

Risk: Incorrect parsed action items can create misleading issues or send incorrect notifications.

Mitigation: Confirm generated issues and email parameters before publishing, sending, or marking the meeting workflow complete.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/myd2002/skills/skill-d-create-issues)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [JSON responses, Markdown issue bodies, and HTML email payload parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates Gitea issue and meeting metadata state when invoked with configured credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
