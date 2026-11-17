## Description:

Analyzes images or video from an older adult’s home to identify behaviors associated with loneliness and suggest companionship actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Families and caregivers use the skill to review behavior reports from an older adult’s living space, consider companionship suggestions, and retrieve prior reports. The results describe observed behavior and do not provide a medical diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may upload private home footage for external processing, including when its no-analysis option is used.

Mitigation: Use non-sensitive test footage until the no-analysis option is fixed. Before sending home recordings, obtain informed consent and confirm the provider’s deletion practices.

Risk: The skill automatically saves account credentials and may enroll a default user.

Mitigation: Review automatic enrollment and token storage before use; avoid sending sensitive footage until these practices are understood.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-elderly-loneliness-comfort-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [API documentation](artifact/references/api_doc.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Guidance]

**Output Format:** [Structured behavior analysis with companionship suggestions and report links; Markdown tables for report listings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include behavioral indicators, a 0–100 loneliness index, and suggested actions; not a medical diagnosis.]

## Skill Version(s):

1.0.11 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
