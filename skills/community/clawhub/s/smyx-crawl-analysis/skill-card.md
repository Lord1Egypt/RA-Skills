## Description:

Analyzes reptile and arachnid videos through a server-side service and returns a structured health report with potential concerns and care suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners can submit a local reptile or arachnid video, or a video URL, to receive an initial health screening report. The report offers potential health indicators and care suggestions; the skill documentation says it does not replace diagnosis by a qualified veterinarian.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary rates the release suspicious and says the scan was partial; it flags possible credential disclosure, shared access to report history, and video transmission without clear notice.

Mitigation: Review the skill before use. Avoid sharing credentials or sensitive footage, and confirm how video uploads and report-history access are handled before submitting personal material.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/smyx-sunjinhui/skills/smyx-crawl-analysis)
- [API interface notes](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured JSON health report; Markdown table for historical reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include potential health indicators, warnings, care suggestions, and report links.]

## Skill Version(s):

1.0.20 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
