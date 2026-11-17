## Description:

Fetches current 新闻联播 hotspot data from the disclosed ClawHub hotspot API and shows titles grouped by source.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xltang](https://clawhub.ai/user/xltang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve current 新闻联播 hotspot data, check service status, and display source-grouped titles without ranking or fabricating unavailable content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches live hotspot data from hotspot.api4claw.com.

Mitigation: Install only when access to the disclosed external API is acceptable for the deployment environment.

Risk: Optional cron setup can create scheduled updates that persist until removed.

Mitigation: Review the cron command before approval and remove the scheduled task when recurring updates are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xltang/skills/xwlb)
- [Hotspot API base URL](https://hotspot.api4claw.com)
- [Hotspot API endpoint](https://hotspot.api4claw.com/hotspots/platform/新闻联播?timestamp=$TIME_STEMP)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with source-grouped text and optional bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API status counts and optional user-approved cron setup commands; does not display fetched_at or data_date.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
