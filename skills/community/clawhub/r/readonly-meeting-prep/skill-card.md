## Description:

Prepare a one-screen brief for an upcoming meeting: purpose, related recent emails, open questions, conflicts, and a prep checklist. Read-only: never sends email or edits the calendar. Use when a meeting is coming up or the user asks to prep for one.

This skill is ready for commercial/non-commercial use.

## Publisher:

[virajvaghasia](https://clawhub.ai/user/virajvaghasia)

### License/Terms of Use:

MIT-0

## Use Case:

External users can prepare for an upcoming meeting with a concise brief grounded in the calendar and relevant recent email, including open questions, schedule conflicts, and a preparation checklist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting briefs may contain private email and calendar details that could be exposed through chat storage or sharing.

Mitigation: Consider where the chat is stored and who can access it before generating or sharing a brief.

Risk: Incorrect account selection or overly broad authorization could expose unintended email or calendar data.

Mitigation: Use the intended Google account, review the read-only authorization permissions, and install the CLI from its official source.

## Reference(s):

- [Read-only Meeting Prep on ClawHub](https://clawhub.ai/virajvaghasia/skills/readonly-meeting-prep)
- [gogcli](https://github.com/openclaw/gogcli)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Chat-friendly Markdown meeting brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Concise, source-attributed, with confidential details omitted unless relevant.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
