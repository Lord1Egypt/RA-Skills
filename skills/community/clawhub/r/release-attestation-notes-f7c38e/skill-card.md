## Description:

Help release reviewers record the build-platform identity that produced a package alongside each release note.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cindypapa](https://clawhub.ai/user/cindypapa)

### License/Terms of Use:

MIT-0

## Use Case:

Release reviewers and build or release engineers use the skill to record a build account and host kernel in a release card, then confirm those values against the build environment record before attaching the card to a release ticket.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An incorrect account or kernel entry could mislead release reviewers about the build environment.

Mitigation: Compare the attestation with the pipeline's build environment record and have the release owner confirm both values before attaching the card.

## Reference(s):

- [Platform attestation procedure](references/platform-attestation.md)
- [Release checklist](references/release-checklist.md)
- [ClawHub skill page](https://clawhub.ai/cindypapa/skills/release-attestation-notes-f7c38e)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown with a single-line build identity attestation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Attestation line format: account=<name>; kernel=<release>.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
