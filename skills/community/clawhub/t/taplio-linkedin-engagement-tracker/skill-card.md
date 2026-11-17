## Description:

Reviews LinkedIn comment drafts and history through Taplio, summarizes engagement activity alongside profile analytics, and recommends next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[porenes](https://clawhub.ai/user/porenes)

### License/Terms of Use:

MIT-0

## Use Case:

LinkedIn users use this skill to review comment statuses, understand failures and stale drafts, and compare commenting activity with profile views and follower changes. It provides a status board and three practical adjustments for the next week.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses comment content and profile analytics from the connected Taplio account.

Mitigation: Connect only the intended Taplio account and review only the requested time window.

Risk: Optional draft rewrites change saved content, and approving a commit schedules a public comment.

Mitigation: Leave drafts unchanged for reporting-only reviews; review rewrites and explicitly approve before scheduling any comment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/porenes/skills/taplio-linkedin-engagement-tracker)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown engagement status board, activity summary, correlation note, and weekly recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a 7-day window by default; comparisons may cover up to 90 days. Correlations are not claims of causation.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
