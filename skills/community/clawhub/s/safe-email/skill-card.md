## Description:

Privacy-first workflow for processing explicitly forwarded emails via IMAP in a dedicated inbox.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nitansde](https://clawhub.ai/user/nitansde)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to process a latest explicitly forwarded email from a dedicated inbox, extract structured details, and receive safe suggested next steps without automatic downstream actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires IMAP credentials for a dedicated inbox.

Mitigation: Use a dedicated email account and provide the app password only through secure runtime configuration.

Risk: Email deletion or expunge can remove the processed message irreversibly.

Mitigation: Request deletion only with explicit user consent and only when the processed email should be removed.

Risk: Processing unrelated inbox messages could expose unnecessary personal data.

Mitigation: Run only after an explicit trigger and read only the newest relevant forwarded message.

## Reference(s):

- [Safe Email ClawHub skill page](https://clawhub.ai/nitansde/skills/safe-email)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown structured summary with ambiguities and suggested next actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sender, subject, time window, location, links, key notes, actionable items, confidence notes, and consent-gated deletion status.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
