## Description:

Same tool as the ironheights skill. Security scanner for skills. Use before installing any skill from ClawHub or GitHub: flags malware, pipe-to-shell, encoded payloads, credential theft.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frank-masciopinto](https://clawhub.ai/user/frank-masciopinto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use the scanner to inspect skills before installation and summarize security findings, verdicts, and recommended next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A clean scan cannot guarantee that a skill is safe.

Mitigation: Treat scan results as one input and review the skill before enabling it.

Risk: The npm executable itself was not audited in this assessment.

Mitigation: Use the pinned CLI from its declared source and assess the executable separately.

Risk: Optional model review may share skill text with a server.

Mitigation: Consider what text would be shared before enabling optional model review.

## Reference(s):

- [ClawHub Malicious Skills Report (October 2026)](https://www.ironheights.dev/reports/clawhub-malicious-skills-2026-10/)
- [Ironheights website](https://www.ironheights.dev)
- [Ironheights ClawHub listing](https://clawhub.ai/frank-masciopinto/skills/ironheights)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON]

**Output Format:** [JSON scan results with plain-language findings and recommended actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings and recommendations vary with the scanned skill and scan verdict.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
