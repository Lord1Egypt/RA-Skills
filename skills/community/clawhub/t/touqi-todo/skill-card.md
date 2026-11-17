## Description:

Touqi Todo helps users organize important life matters such as wishes, instructions, account handoffs, personal messages, visibility boundaries, progress reviews, and optional PDF exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ezra-y](https://clawhub.ai/user/ezra-y)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to capture, classify, organize, and review sensitive end-of-life notes, digital estate handoff details, personal messages, and audience-specific visibility boundaries. The skill can optionally help prepare a PDF export when the user explicitly requests it and the content is ready.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt users to record passwords, recovery codes, private keys, API tokens, MFA secrets, or similarly sensitive account material.

Mitigation: Do not enter raw secrets into the skill; use a password manager or secure estate-planning process for credential handoff.

Risk: The skill handles deeply private end-of-life information and may label content as visible, hidden, isolated, masked, or excluded.

Mitigation: Treat visibility labels as organizational notes unless the hosting platform provides verified encryption, retention, deletion, and sharing controls.

Risk: The skill can produce an optional PDF export containing sensitive personal information.

Mitigation: Generate exports only on explicit request, review the contents before sharing, and store or delete exported files according to the user's privacy requirements.

## Reference(s):

- [Server-resolved source repository](https://github.com/Ezra-Y/touqi-todo)
- [ClawHub skill page](https://clawhub.ai/ezra-y/skills/touqi-todo)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown text with structured notes, status summaries, visibility labels, and optional PDF export guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May classify entries by type, audience, and completion state; PDF export is optional and only on explicit request.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
