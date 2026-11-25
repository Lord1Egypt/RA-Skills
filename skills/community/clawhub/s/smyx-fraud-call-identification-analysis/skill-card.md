## Description:

Analyzes call content for fraud indicators, assesses risk, and produces an Anti-Fraud Guardian analysis report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

People reviewing suspected scam calls use the skill to analyze recordings or transcripts, assess fraud risk, and receive recommendations and report links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious with high confidence, citing undeclared account and credential handling.

Mitigation: Verify the publisher and service, and review local identity and credential handling before installation; avoid running it where stored credentials cannot be protected.

Risk: Call media and identity information may be exposed through remote processing, according to the security assessment.

Mitigation: Confirm the remote service's privacy and retention practices, and submit recordings or transcripts only when you have authority to share them.

Risk: The security assessment reports a mismatch between the fraud-call description and some reported capabilities, and notes that scanner coverage was incomplete.

Mitigation: Review the full release contents and have the missing referenced material checked before relying on the skill.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-fraud-call-identification-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [API documentation](references/api_doc.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Markdown, Guidance]

**Output Format:** [Structured fraud-risk report with findings, risk level, recommendations, and report links when available; JSON or Markdown output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports analysis of call text or media and can list prior reports.]

## Skill Version(s):

9.9.24 (source: server-resolved release metadata; artifact frontmatter reports 1.0.26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
