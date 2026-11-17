## Description:

Analyzes IT procurement opportunities using historical bid data to recommend whether to bid, identify likely competitors and pricing ranges, and flag qualification risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liu-jiapeng](https://clawhub.ai/user/liu-jiapeng)

### License/Terms of Use:

MIT-0

## Use Case:

Bid teams and other external users assess Chinese IT and localization procurement opportunities, comparing buyer history, likely competitors, past award prices, and bid requirements before deciding whether and how to bid.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project and company queries are sent to a third-party bid-data service.

Mitigation: Review queries for confidential information before sending them to the service.

Risk: Analysis consumes paid API credits.

Mitigation: Review the estimated credit cost before starting and choose the shorter analysis when appropriate.

Risk: Optional trial registration sends a hashed device identifier and may store an API key locally.

Mitigation: Set your own ZLBX_API_KEY to avoid automatic registration and local key persistence; otherwise consent to registration only after reviewing these terms.

Risk: Generated bid and pricing conclusions may rely on incomplete or delayed records.

Mitigation: Check cited notices, data gaps, and bid documents before making a commercial decision.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/liu-jiapeng/skills/xinchuang-it-bid-decision)
- [ClawHub publisher profile](https://clawhub.ai/user/liu-jiapeng)
- [Skill documentation](https://ai.zhiliaobiaoxun.com/docs/skill)
- [Bid analysis workflow](references/workflow.md)
- [Report template](references/report-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML report file, Guidance]

**Output Format:** [Markdown decision report in chat; HTML report file in full mode]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a bid recommendation, pricing reference, competitor analysis, risk list, and source and data-gap notes.]

## Skill Version(s):

1.0.7 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
