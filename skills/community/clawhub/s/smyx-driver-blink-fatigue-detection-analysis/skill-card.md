## Description:

Analyzes driver-facing video for blink rate, eye-closure duration, and visual fatigue warnings, with access to historical analysis reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Fleet operators and developers use the skill to review driver-facing video for possible fatigue indicators and retrieve historical monitoring reports. Visual alerts are not medical diagnoses or a substitute for driver attention.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Driver face/video data or video URLs are sent to a configured cloud service.

Mitigation: Obtain driver consent and confirm the service's data retention, deletion, and report access policies before use.

Risk: Automatic identity creation or reuse and locally stored access tokens and user/profile data can persist across sessions.

Mitigation: Review cloud account linkage and restrict access to local credentials and reports, especially on shared devices.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/smyx-sunjinhui/skills/smyx-driver-blink-fatigue-detection-analysis)
- [API interface reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured analysis results and Markdown report listings with links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional saved result file; visual fatigue indicators and directional alerts, not medical diagnoses.]

## Skill Version(s):

1.0.12 (source: server-resolved ClawHub release; artifact frontmatter lists 1.0.18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
