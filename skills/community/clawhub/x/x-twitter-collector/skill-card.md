## Description:

Automatically collects public X/Twitter posts for a specified user over a recent time window and produces a bilingual report with tweet links, engagement data, topic summaries, and screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pinotao](https://clawhub.ai/user/pinotao)

### License/Terms of Use:

OpenClaw Skill License Agreement

## Use Case:

Developers, analysts, and communications teams use this skill to review recent public X/Twitter activity from selected accounts and turn it into a bilingual monitoring or summary report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use a logged-in browser session to view X pages.

Mitigation: Use a browser profile and X account appropriate for the review task, and collect only accounts the user is permitted to review.

Risk: Generated reports and full-page screenshots may retain public tweet content, links, engagement counts, and visible page context on disk.

Mitigation: Review and clean the configured report and media directories when archived copies are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pinotao/skills/x-twitter-collector)
- [Publisher profile](https://clawhub.ai/user/pinotao)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown report with bilingual tables, tweet links, engagement metrics, topic summaries, and optional PNG screenshots.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default collection window is 24 hours; reports and screenshots may be saved to local report and media directories.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact config)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
