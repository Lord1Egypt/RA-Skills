## Description:

Retrieves the user's saved Signatoro signature and appends it to email drafts and outgoing messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m-viable](https://clawhub.ai/user/m-viable)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams using AI email assistants can append their saved Signatoro signature to drafts, replies, forwards, and outgoing messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The assistant contacts Signatoro when preparing email and may append signature content containing links, images, or tracking-sensitive elements.

Mitigation: Enable only when this contact is intended; review the saved signature and its links or images before use.

Risk: Exposure of the Signatoro API key could grant unauthorized access to the account's signature data.

Mitigation: Keep SIGNATORO_API_KEY private and appropriately scoped; do not include it in messages, files, or logs.

## Reference(s):

- [Signatoro agent installation guide](https://signatoro.com/docs/install-signature/agent)
- [ClawHub skill listing](https://clawhub.ai/m-viable/skills/signatoro-email-signature)

## Skill Output:

**Output Type(s):** [Text, HTML]

**Output Format:** [Plain-text or HTML email body with appended signature]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the saved signature returned by Signatoro; sends without one if unavailable.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
