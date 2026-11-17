## Description:

Guides agents through Tonglian terminal requests and sub-merchant onboarding by collecting merchant and store data, preparing standardized Excel application forms and email drafts, and requiring user confirmation before sending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shouqianba](https://clawhub.ai/user/shouqianba)

### License/Terms of Use:

MIT-0

## Use Case:

Operations and merchant support staff use this skill to prepare Tonglian POS terminal applications and sub-merchant additions for new stores, including merchant-number lookup, Excel form preparation, email drafting, and pre-send confirmation.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Merchant and contact data can be included in generated forms and email drafts.

Mitigation: Review forms and email text before approving send; only proceed when the user explicitly confirms.

Risk: Application materials can be sent to an external Tonglian payment contact.

Mitigation: Verify recipients and attachments before sending, and do not send empty or incomplete emails.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shouqianba/skills/tonglian-terminal-application)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Excel files plus concise text or Markdown email drafts and confirmation messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before sending application email; generated forms should preserve the provided Excel templates.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
