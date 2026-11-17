## Description:

Analyzes driver-facing video for facial flushing and abnormal sweating and returns health-risk reminders and analysis reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Drivers and authorized fleet operators use this skill to analyze in-cabin video for visible flushing and sweating, review health-risk reminders, and retrieve past reports. The alerts support awareness and do not provide medical diagnoses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Driver face video or video URLs are sent to configured lifeemergence.com services.

Mitigation: Review the destination before installation and obtain explicit consent from affected drivers before sending video.

Risk: The skill creates or reuses an internal identity and stores identity and token data in the workspace data directory.

Mitigation: Restrict access to the workspace data directory and review identity and token handling before use.

Risk: History queries can expose sensitive face and health-related reports.

Mitigation: Limit report queries to operators authorized to view those records and avoid unnecessarily broad queries.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/smyx-sunjinhui/skills/smyx-driver-flushing-sweat-detection-analysis)
- [API interface documentation](references/api_doc.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Structured analysis text and JSON results; Markdown tables and report links for history queries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save results to a file when requested.]

## Skill Version(s):

1.0.13 (source: ClawHub server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
