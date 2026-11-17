## Description:

Analyzes fixed-camera video from public venues to summarize facial-expression categories and a 0–100 group emotion index.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

External venue operators and their developers can use the skill to review fixed-camera footage and receive aggregate emotion metrics, trends, and suggested operational or safety follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports that local video may be sent to an external service.

Mitigation: Before providing footage, confirm the venue is authorized to share it with that service and review the service's processing and retention terms.

Risk: The security assessment flags undisclosed account and credential handling, including account or token creation and retention.

Mitigation: Review the account and token lifecycle before use, use only approved scoped credentials, and avoid submitting secrets until handling is understood.

Risk: The security assessment says some behavior may not clearly match the described emotion analysis; the scan was partial, with a referenced local path missing and delegated behavior unassessed.

Mitigation: Review the complete package and any delegated components before use, and do not rely on its outputs until the behavior is understood.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-public-place-group-emotion-index-analysis)
- [API reference](artifact/references/api_doc.md)
- [Skill demo](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured JSON analysis reports and Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Aggregate emotion distributions and group index, with possible regional breakdowns, trends, suggestions, and report links; outputs are described as group-level results.]

## Skill Version(s):

1.0.18 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
