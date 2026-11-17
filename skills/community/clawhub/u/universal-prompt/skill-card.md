## Description:

A bilingual preview prompt skill that helps agents produce enterprise software sales coaching, outreach, objection handling, proposal, and follow-up guidance from a To B sales playbook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijian417](https://clawhub.ai/user/lijian417)

### License/Terms of Use:

MIT-0

## Use Case:

External sales teams and agent users can use this skill to generate structured B2B enterprise software sales advice, discovery questions, follow-up language, objection handling, and deal-next-step guidance in Chinese or English.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reduce answer depth after a small free allowance and route users toward a paid upgrade.

Mitigation: Review and, if needed, remove or rewrite the preview gating and upgrade messaging before deployment.

Risk: The skill references QR-based payment or paid-channel unlocking without a verified destination in the evidence.

Mitigation: Do not scan or pay through any QR code unless the publisher and payment destination are independently verified.

Risk: The release license is inconsistent across evidence sources.

Mitigation: Confirm the authoritative license before distributing or using the skill in a governed environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lijian417/skills/universal-prompt)
- [Publisher profile](https://clawhub.ai/user/lijian417)
- [Skill definition](artifact/SKILL.md)
- [English universal prompt](artifact/system-prompt-en.md)
- [Chinese universal prompt](artifact/system-prompt-zh.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance and reusable prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese and English sales coaching content; preview behavior may shorten responses after a small free allowance and append paid-upgrade messaging.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
