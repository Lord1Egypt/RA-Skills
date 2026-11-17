## Description:

A practical self-report security review skill that checks crypto wallet and backup habits for obvious weak points.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to self-audit crypto wallet security habits, backup practices, account protections, device hygiene, and phishing exposure. It helps prioritize theft-risk and recovery-risk fixes based on information the user chooses to share.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may disclose sensitive wallet recovery material or precise backup details while answering the checklist.

Mitigation: Ask only about habits and storage methods; do not request seed phrases, private keys, passwords, exact backup locations, recovery codes, or other secrets.

Risk: The skill cannot verify the real security posture of a device, wallet, account, or backup.

Mitigation: Present results as a self-report discussion checklist and mark unknown areas as unknown rather than safe.

Risk: Incomplete answers can lead to an overly confident safety snapshot.

Mitigation: State uncertainty plainly and prioritize fixes by impact and ease instead of claiming forensic certainty.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown checklist with a safety snapshot, top risks, prioritized actions, and a monthly re-check list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Self-report only; no real-time scanning, wallet inspection, account inspection, or forensic validation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
