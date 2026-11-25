## Description:

Analyzes a home-arrival video for possible signs of after-work fatigue and returns a structured summary with gentle self-care suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

External smart-home users can use the skill to review a short home-arrival video for possible fatigue indicators and receive gentle self-care suggestions; it is not a medical assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags possible remote handling of private household footage.

Mitigation: Use only footage you have permission to share, and review the service's privacy and data-handling terms before sending household video.

Risk: The security review flags possible silent account creation and credential storage.

Mitigation: Review account setup and credential handling before use, and avoid providing credentials you are not comfortable storing with the service.

Risk: The security review warns that an export-only option may still analyze video.

Mitigation: Do not use export-only mode with private footage unless its behavior has been confirmed for the installed release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-commuter-fatigue-care-analysis)
- [API reference](artifact/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Recommendations]

**Output Format:** [Structured analysis report, with Markdown tables for history listings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include observed fatigue indicators, a fatigue score, care suggestions, and report links; it does not provide a medical diagnosis.]

## Skill Version(s):

1.0.17 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
