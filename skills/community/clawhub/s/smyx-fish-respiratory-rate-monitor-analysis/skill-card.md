## Description:

Analyzes aquarium footage of fish gill movement, estimates respiratory rate, and reports potential anomalies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Aquarium owners, aquaculture operators, and aquarium or laboratory staff can use the skill to review fish footage for gill movement, respiratory-rate estimates, and possible breathing abnormalities. It can also retrieve previously generated monitoring reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags identity and credential handling and remote services beyond the fish-analysis task; some referenced components were not reviewed.

Mitigation: Before use, clarify which video and identity data is sent, what is stored, who may receive alerts, and review the unexamined components.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-fish-respiratory-rate-monitor-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured monitoring report with respiratory-rate estimates, anomaly flags, suggested checks, and report links; history can be presented as a Markdown table.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are visual monitoring estimates and recommendations, not a diagnosis; the skill documentation prohibits specific medication advice.]

## Skill Version(s):

1.0.14 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
