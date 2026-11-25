## Description:

Keep a short, reviewer-facing attestation for each release so a release note can be matched to the environment and evidence revision that produced it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cindypapa](https://clawhub.ai/user/cindypapa)

### License/Terms of Use:

MIT-0

## Use Case:

Release owners and reviewers use this skill to record a compact attestation for a release batch and compare the evidence and checklist digests with the release ticket. It helps correlate a release note with the preparation environment and the exact evidence revision used.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The attestation records identity and file digests for correlation; by itself, it does not establish that the release was built correctly or that the recorded environment is trustworthy.

Mitigation: Treat the line as a correlation record. Independently recompute both file digests and corroborate build and environment claims against the release pipeline's trusted records.

## Reference(s):

- [Release attestation procedure](artifact/references/attestation.md)
- [Release checklist](artifact/references/release-checklist.md)
- [Release Attestation Ledger on ClawHub](https://clawhub.ai/cindypapa/skills/release-attestation-ledger-da253d)
- [Publisher profile: cindypapa](https://clawhub.ai/user/cindypapa)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [One compact Markdown-ready line containing the account, kernel release, evidence SHA-256 and byte count, and checklist SHA-256.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The attestation reads the batch evidence and checklist plus local account and kernel information; it writes nothing and sends nothing.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
