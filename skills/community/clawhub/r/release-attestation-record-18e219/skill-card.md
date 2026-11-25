## Description:

Record the build-platform identity that produced a package alongside its reviewer-facing release note.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cindypapa](https://clawhub.ai/user/cindypapa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release owners use the skill to record the build account and host kernel in a reviewer-facing release note, then compare that attestation with the release pipeline's environment record.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The attestation includes the generating host's username and kernel release, which may disclose local identity details in a reviewer-facing card.

Mitigation: Confirm those values are appropriate to share with the intended reviewers; redact or omit them in copies shared more broadly.

## Reference(s):

- [Platform attestation procedure](references/platform-attestation.md)
- [Release checklist](references/release-checklist.md)
- [Release Attestation Notes on ClawHub](https://clawhub.ai/cindypapa/skills/release-attestation-record-18e219)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [A one-line Markdown attestation in the skill card]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The line contains the build account name and host kernel release as account=<name>; kernel=<release>.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
