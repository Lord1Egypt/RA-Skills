## Description:

Analyzes crop leaf, bud, and fruit images or videos to identify common pests and report pest types with confidence scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Farmers and agricultural practitioners can analyze crop images or videos to identify common pests, estimate counts, and review confidence scores for early detection. Results are for reference and do not include pesticide or pest-control recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flags account and profile handling, report-history retrieval, file writing, and analysis that may continue when an option says not to analyze. The scan is partial because a referenced local path was missing.

Mitigation: Avoid installation until these behaviors are clearly explained. If used, assume local media may be sent to a remote service and avoid relying on an option alone to prevent analysis.

Risk: Identity or token data may be stored or transmitted while processing images or videos.

Mitigation: Use only media you are authorized to share and review the service's identity and data-handling behavior before use.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Skill introduction demo](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Structured pest identification report or Markdown table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include pest types, estimated counts, affected plant parts, confidence scores, and report links.]

## Skill Version(s):

1.0.16 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
