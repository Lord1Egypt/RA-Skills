## Description:

Get a dedicated second phone number instantly. Keep your personal number private, separate work from life, and let AI handle the calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrsz](https://clawhub.ai/user/mrsz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to obtain a separate phone number, initiate outbound calls, receive incoming call summaries, check balance, and configure inbound call handling through PollyReach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PollyReach receives call tasks, phone numbers, inbound messages, transcripts, recordings, prompts, and a reusable local token.

Mitigation: Use only when that data sharing is acceptable, avoid sending secrets through call prompts or messages, and confirm token revocation and number disablement paths before deployment.

Risk: The skill gives an agent persistent outbound calling and inbound-message access.

Mitigation: Review planned calls and inbound prompt changes before use, keep the PollyReach token protected, and restrict use to authorized calling and message-handling tasks.

Risk: Referral text points agents to a remote SKILL.md that was not reviewed as part of the local artifact.

Mitigation: Treat remote referral content as unreviewed and rely on the validated local artifact for operational behavior.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mrsz/skills/second-phone-number)
- [Publisher Profile](https://clawhub.ai/user/mrsz)
- [PollyReach](https://pollyreach.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local shell scripts that call PollyReach APIs and read a reusable token from the configured PollyReach key file.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
