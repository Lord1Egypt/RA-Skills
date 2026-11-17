## Description:

Generates condensed album highlights based on specified keywords or targets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

People organizing family, travel, or event footage can request target-based video analysis and receive structured reports with suggested highlights and report links. They can also retrieve previous analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote analysis may process personal video and prompt data; the available security guidance says data transmission and account/history behavior need clarification.

Mitigation: Confirm the service's data handling and retention practices before submitting sensitive footage.

Risk: The security assessment flags options that may trigger analysis unexpectedly, including uncertainty about whether export-only avoids processing.

Mitigation: Verify option behavior before use and do not assume export-only prevents analysis.

Risk: The security assessment reports partial review coverage because a referenced local path was missing.

Mitigation: Review the complete release contents and resolve missing referenced material before installation.

## Reference(s):

- [API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-custom-timelapse-analysis)

## Skill Output:

**Output Type(s):** [Analysis reports, JSON, Markdown]

**Output Format:** [Structured analysis report in text or JSON; history lists can be presented as Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analysis detail can be basic, standard, or JSON; results may include suggestions and report links.]

## Skill Version(s):

1.0.18 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
