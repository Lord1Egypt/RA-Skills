## Description:

Send a quick email via SkillBoss API Hub without a local mail client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quincygunter](https://clawhub.ai/user/quincygunter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to prepare quick email-sending requests through SkillBoss API Hub, including recipients, CC, BCC, subject, and HTML body fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email can be sent to unintended recipients or include sensitive content.

Mitigation: Review recipients, CC/BCC, subject, and HTML body before sending; avoid secrets, regulated data, or sensitive business information unless approved by the organization.

Risk: The skill depends on a third-party email API and an API key.

Mitigation: Install only when SkillBoss API Hub use is approved, and keep SKILLBOSS_API_KEY in the runtime environment rather than source files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quincygunter/skills/qui-email-send)
- [Publisher profile](https://clawhub.ai/user/quincygunter)
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and may include email fields such as receivers, cc, bcc, title, and body_html.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
