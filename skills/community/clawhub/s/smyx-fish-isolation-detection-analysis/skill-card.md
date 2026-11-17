## Description:

Analyzes aquarium footage for schooling and prolonged fish isolation, returning structured findings, alerts, and report links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Aquarists and aquarium or aquaculture operators use the skill to review camera footage for fish separating from a school and to retrieve historical behavior reports. Its alerts support observation and professional follow-up, not disease diagnosis or treatment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Aquarium images or video are sent to external cloud services, potentially exposing sensitive footage.

Mitigation: Use only authorized, nonsensitive footage after checking the service's retention and account controls.

Risk: The skill creates or reuses a service identity and stores access tokens locally.

Mitigation: Protect workspace data/smyx-api-key.txt and the local SQLite database with restricted access; review these files before installation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/smyx-sunjinhui/skills/smyx-fish-isolation-detection-analysis)
- [Fish isolation API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Guidance]

**Output Format:** [Structured text or JSON analysis results; Markdown historical report tables and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save results to a local file; provides isolation findings, alert levels, suggested checks, and report links.]

## Skill Version(s):

1.0.11 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
