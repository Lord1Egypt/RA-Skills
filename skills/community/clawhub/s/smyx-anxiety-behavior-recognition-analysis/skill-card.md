## Description:

Analyzes fixed-camera video to estimate hand-rubbing, nail-biting, and pacing frequency and duration, and provide behavior trends and self-care prompts without diagnosing anxiety.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals may use the skill to review patterns in anxiety-related behaviors, while counselors may use its behavior summaries to support intervention follow-up. Results are visual behavior indicators and are not a medical diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive video may be processed by an API, while its destination and retention details are not provided.

Mitigation: Review the remote processing and retention terms before sending footage, obtain the subject's consent, and avoid uploading sensitive recordings unless needed.

Risk: The scan reports identity transmission during automatic registration and local credential storage.

Mitigation: Review what identity data and credentials are transmitted or stored, and restrict access to local credential files.

Risk: Security scan coverage is incomplete because a referenced path could not be resolved.

Mitigation: Resolve and review the missing path, then repeat the security assessment before deployment.

## Reference(s):

- [ClawHub release](https://clawhub.ai/smyx-sunjinhui/skills/smyx-anxiety-behavior-recognition-analysis)
- [Skill demo](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [Structured behavior analysis results or Markdown reports and history tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include behavior frequency and duration, a behavior index and trends, self-care suggestions, and report links; outputs are not diagnoses.]

## Skill Version(s):

1.0.11 (source: target release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
