## Description:

Check Gmail for unread inbox emails, filtered by priority, and output a brief digest sorted as HIGH, MEDIUM, or LOW while skipping promotions, social, updates, and forums.

This skill is ready for commercial/non-commercial use.

## Publisher:

[99rebels](https://clawhub.ai/user/99rebels)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to check recent unread Gmail inbox messages and receive a concise priority-ranked digest. It is useful for inbox summaries, new-mail checks, and filtering out low-value Gmail categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires read-only Gmail OAuth access and stores a local refresh token.

Mitigation: Use a private SKILL_DATA_DIR or operating-system credential store, keep the token file private, and revoke the Google OAuth grant when the skill is no longer needed.

Risk: OAuth client secrets could be exposed if entered into chat or an untrusted session.

Mitigation: Enter OAuth client secrets only in a local, trusted terminal and do not paste them into agent chat.

Risk: The release was flagged for review because it handles private email with weak disclosure around secrets.

Mitigation: Review the setup flow and security guidance before installation, and grant access only if read-only Gmail access is acceptable.

## Reference(s):

- [Gmail Setup Guide](references/setup.md)
- [ClawHub Skill Page](https://clawhub.ai/99rebels/skills/rebels-gmail-checker)
- [Publisher Profile](https://clawhub.ai/user/99rebels)
- [Google Cloud Console](https://console.cloud.google.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Plain text or JSON email digest, with setup guidance in Markdown and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Digest entries include sender, subject, date, and priority; default lookback is 24 hours and can be configured.]

## Skill Version(s):

1.3.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
