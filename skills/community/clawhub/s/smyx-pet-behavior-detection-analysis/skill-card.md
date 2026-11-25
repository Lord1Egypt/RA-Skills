## Description:

Identifies common abnormal pet behaviors such as scratching, biting, destructive chewing, jumping, digging, chasing, and separation anxiety, helping owners understand their pet's habits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners use the skill to analyze submitted pet videos for common behaviors and receive a structured report with observations, suggestions, and report links. The results are advisory; consult a qualified pet trainer for behavior concerns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags possible remote video uploads and notes that the scan is incomplete.

Mitigation: Submit only footage you are authorized to share; use a non-sensitive test clip first and confirm the service's handling of uploaded footage before sending private recordings.

Risk: The security assessment flags possible account and credential handling, including identity data.

Mitigation: Do not include personal login credentials in prompts or files; use only an API key from a trusted service operator and rotate it if exposed.

Risk: The security assessment warns that the export-only option may still run analysis.

Mitigation: Do not assume export-only avoids processing or remote transmission; review the command output and use it only when analysis is acceptable.

## Reference(s):

- [API interface notes](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured JSON analysis results; Markdown tables for history reports, with report links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include behavior observations, suggestions, and links to view or export results.]

## Skill Version(s):

1.0.19 (source: server-resolved release metadata; artifact frontmatter reports 1.0.26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
