## Description:

Helps agents manage SignNow documents, templates, signature invitations, and related e-signature workflows through a Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can ask an agent to find, upload, and manage SignNow documents and templates or prepare signature invitations. The skill also describes optional, user-approved automation and webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document changes and signature invitations may affect records or notify recipients.

Mitigation: Confirm the target document, recipients, and intended effect before any write.

Risk: Webhooks and trigger destinations can forward event data continuously until deleted.

Mitigation: Review destinations and forwarded data, require separate approval, and remove forwarding when no longer needed.

Risk: Connecting an account grants access to SignNow data through Maton.

Mitigation: Connect only trusted accounts after user approval and limit access to the task's needs.

## Reference(s):

- [SignNow skill release](https://clawhub.ai/byungkyu/skills/signnow)
- [SignNow API reference](https://docs.signnow.com/docs/signnow/reference)
- [Maton](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with command and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions use the user's authorized connection; writes require explicit approval.]

## Skill Version(s):

1.2.6 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
