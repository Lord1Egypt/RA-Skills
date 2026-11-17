## Description:

Analyzes multi-angle pet videos to estimate a 1–9 Body Condition Score and produce a structured observation report; it does not diagnose disease or prescribe treatment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners and developers use the skill to assess a pet's body condition from local or linked multi-angle video and review a structured report. It can also retrieve prior reports through the service; results are for weight-management reference and should not replace veterinary assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags privacy, identity, and account-handling concerns, including unexpected history retrieval; the scan is partial.

Mitigation: Review the reported behavior before use, especially in shared workspaces, and avoid submitting private video until you understand how it is handled.

Risk: The security evidence reports that a no-analysis option may still run analysis.

Mitigation: Use the skill only with an explicit analysis input and check the resulting behavior before relying on it.

## Reference(s):

- [API interface reference](artifact/references/api_doc.md)
- [API error codes](artifact/skills/smyx_analysis/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-pet-body-condition-score-3d-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured body-condition report as JSON or Markdown, including a BCS estimate, body-type classification, observations, and report links when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Visual estimate for weight-management reference; does not diagnose disease or prescribe treatment.]

## Skill Version(s):

1.0.15 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
