## Description:

Analyzes fry images or video containing a known-size reference object to estimate body length and growth over time, then produces growth statistics, curves, and alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Aquaculture workers and ornamental fish breeders use the skill with periodic fry images or video to track body length and growth, review population statistics, and receive growth alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan flags identity and credential handling beyond the stated growth-analysis purpose, and possible remote analysis during export-only use; its scan was partial and does not establish that the skill is safe.

Mitigation: Before installing, verify why identity and credentials are handled, where media and identity data are sent, and whether export-only use triggers remote analysis.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/smyx-sunjinhui/skills/smyx-fish-fry-growth-measurement-analysis)
- [API reference](references/api_doc.md)
- [Skill demo](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured JSON and Markdown growth reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Body-length measurements, growth rates, population statistics, growth curves, alerts, and suggested actions.]

## Skill Version(s):

1.0.17 (source: server-resolved release; artifact frontmatter lists 1.0.23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
