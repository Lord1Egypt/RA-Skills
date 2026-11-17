## Description:

Analyzes video of older adults living alone to summarize observable behaviors associated with loneliness or depressive tendencies and produce emotional-risk reports for caregivers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Family members, care staff, and community workers can use the skill to review video-based summaries of observable behavior and receive prompts for follow-up care. It is a behavioral support aid and does not provide depression screening or diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive video may be sent to an analysis service without clear disclosure, and account or credential handling is not clearly explained.

Mitigation: Before installation, ask the author to clarify account and token handling, where footage is sent, and how it is retained; obtain the older adult's informed consent and protect footage as recommended in the skill documentation.

Risk: The export-only option may still run analysis.

Mitigation: Avoid relying on export-only behavior until the author fixes or documents it.

Risk: The security assessment is incomplete: one of 29 components was not inspected and one static analysis was degraded.

Mitigation: Treat the scan as incomplete and seek clarification and review before installation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/smyx-sunjinhui/skills/smyx-elderly-loneliness-depression-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured JSON analysis results and Markdown report summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include behavior counts and durations, baseline comparisons, risk-level prompts, recommendations, and report links; results are behavior-based and are not a medical diagnosis.]

## Skill Version(s):

1.0.14 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
