## Description:

Analyzes images or video of pet enclosure floors to estimate waste coverage, assess cleanliness, and report when a threshold is exceeded.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Pet boarding, retail, veterinary, and breeding facility staff use the skill to review enclosure cleanliness from camera images or video and prioritize cleaning when detected waste exceeds a set threshold.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious with high confidence, citing credential handling, external requests, and unclear handling of local media; scan coverage was partial and did not verify the stated detection and alert workflow.

Mitigation: Review the publisher, credential use, external destinations, and media-transfer behavior before installing, and independently confirm the detection and alert workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-cage-cleanliness-detection-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [API reference](artifact/references/api_doc.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured cleanliness analysis report with measurements, findings, and cleaning alerts; Markdown table for history results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Visual estimates depend on image or video clarity; results are for environmental hygiene management and are not medical advice.]

## Skill Version(s):

1.0.17 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
