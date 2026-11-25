## Description:

Analyzes fixed-camera workplace videos for group-level stress signals by office zone and returns heatmaps and structured reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Enterprise workplace health, HR, and facilities teams use it to review aggregate patterns across office zones and inform organizational wellness decisions. Results are described as group-level indicators, not individual assessments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workplace video handling and account-related behavior raise privacy and scope concerns; scanner coverage is partial because a referenced path was missing.

Mitigation: Before use, review the video trigger and destination behavior, confirm authorization and employee notice or consent, and verify that results remain zone-level and that video retention matches policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-workplace-stress-heatmap-analysis)
- [API reference](artifact/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured JSON analysis reports and Markdown report lists, with heatmap and report links where available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Zone-level aggregate indicators, trends, alerts, and suggested actions; the skill documentation specifies a minimum sample threshold before returning a zone score.]

## Skill Version(s):

1.0.15 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
