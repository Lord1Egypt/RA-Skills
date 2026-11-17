## Description:

Analyzes videos of pets left alone to identify possible separation-anxiety behaviors and provide severity estimates, calming suggestions, and structured reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners, frequent travelers, and boarding staff can use it to review video of pets left alone and receive behavior observations with calming suggestions. Its results are for behavior observation and are not a veterinary diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Household videos may be sent for external analysis.

Mitigation: Use only clips you are comfortable sharing, avoid capturing people or private areas, and obtain consent from anyone recorded.

Risk: The skill handles automatic account registration and local token storage.

Mitigation: Review account and credential handling before use; use a dedicated account and protect the local environment and token files.

Risk: ClawScan marks the skill suspicious, and its scan is partial with a missing local path and unverified imported components.

Mitigation: Review the skill carefully and resolve the missing path and unverified components before installation.

Risk: Scanners report behavior that differs from the pet-monitoring description.

Mitigation: Inspect the skill's behavior and data handling before execution.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-separation-anxiety-relief-analysis)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Markdown, Guidance]

**Output Format:** [Structured analysis report in text or JSON; Markdown for report listings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include behavior observations, severity estimates, calming suggestions, and report links.]

## Skill Version(s):

1.0.15 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
