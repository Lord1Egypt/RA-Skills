## Description:

Helps validate that agent behavior at runtime matches the capabilities and constraints declared in its attestation, detecting divergence between claimed and observed behavior during execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud)

### License/Terms of Use:


## Use Case:

Developers, security reviewers, and trust-and-safety teams use this skill to evaluate whether an agent skill's runtime behavior matches its declared attestation. It supports review of capability boundaries, conditional activation, data handling, side effects, and attestation drift.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime probing may execute untrusted or destructive skill behavior.

Mitigation: Run probes only in isolated sandboxes with test credentials and non-production data.

Risk: Conditional behavior may require runtime conditions that are absent from the probe environment.

Mitigation: Use varied controlled environments and treat clean results as coverage-limited rather than proof of absence.

Risk: Legitimate environment-dependent behavior can resemble suspicious conditional activation.

Mitigation: Require human review of surfaced behavioral differences before classifying them as malicious or functional.

## Reference(s):

- [Runtime Attestation Probe on ClawHub](https://clawhub.ai/andyxinweiminicloud/skills/runtime-attestation-probe)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report guidance with structured verdicts and scores]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a runtime attestation report with boundary findings, conditional behavior patterns, data-flow checks, side-effect inventory, drift score, and a verdict.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
