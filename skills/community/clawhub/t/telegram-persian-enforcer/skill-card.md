## Description:

Helps agents write natural Persian messages for Telegram and check drafts for leftover Latin words and Western numerals before sending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ehsanghaffar](https://clawhub.ai/user/ehsanghaffar)

### License/Terms of Use:

MIT-0

## Use Case:

Agents preparing Telegram replies, notifications, reports, captions, and button text use this skill to write fluent Persian and review drafts before sending. A user can explicitly request another language for an individual message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Draft checks can miss unnatural wording or Latin text in exempted spans.

Mitigation: Review the final message for fluency and exemptions as well as running the strict draft check.

Risk: Using --pending writes proposed terms to a local review file.

Mitigation: Review proposed terms before approving them; pending entries do not automatically become allowed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ehsanghaffar/skills/telegram-persian-enforcer)
- [ClawHub publisher profile](https://clawhub.ai/user/ehsanghaffar)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Persian Telegram-ready messages and draft review feedback]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves code, URLs, and identifiers where appropriate; the checker flags issues but does not translate or assess prose quality.]

## Skill Version(s):

1.0.5 (source: server-resolved ClawHub release; artifact frontmatter lists 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
