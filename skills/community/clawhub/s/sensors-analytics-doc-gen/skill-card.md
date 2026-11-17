## Description:

Converts Chinese Sensors Analytics manual content into standardized Feishu usage documents for supported analytics and metadata modules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bianca1227](https://clawhub.ai/user/bianca1227)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and documentation teams use this skill to turn Sensors Analytics manual pages into consistent Feishu how-to documents. It supports analytics, dashboard, audience, and metadata management modules and asks users to confirm the document framework before generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated markdown or internal edits may be sent to Feishu.

Mitigation: Confirm that Feishu is approved for the intended manual content, internal edits, and business context before using the skill.

Risk: The skill fetches user-provided manual links as part of document generation.

Mitigation: Use Sensors Analytics manual URLs for the source material and review fetched content before creating the Feishu document.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bianca1227/skills/sensors-analytics-doc-gen)
- [Sensors Analytics event analysis manual](https://manual.sensorsdata.cn/sa/docs/guide_analytics_event)
- [Sensors Analytics retention analysis manual](https://manual.sensorsdata.cn/sa/docs/guide_analytics_retention)
- [Sensors Analytics funnel analysis manual](https://manual.sensorsdata.cn/sa/docs/guide_analytics_funnel)
- [Sensors Analytics metadata manual](https://manual.sensorsdata.cn/sa/docs/guide_metadata_meta/v0205)
- [Sensors Analytics user group manual](https://manual.sensorsdata.cn/sa/docs/User_Group_Create/v0205)

## Skill Output:

**Output Type(s):** [Markdown, API Calls, Guidance]

**Output Format:** [Markdown content for a Feishu document, with confirmation prompts and generated document metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may fetch user-provided Sensors Analytics manual pages and send generated markdown to Feishu.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
