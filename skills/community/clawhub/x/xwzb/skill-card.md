## Description:

新闻早报 fetches Chinese-language hotspot and news items from hotspot.api4claw.com, summarizes top items, groups titles by source, reports service status, and can provide a user-approved cron setup command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xltang](https://clawhub.ai/user/xltang)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to request the latest Chinese-language hotspot items, service status, source-grouped titles, or a source-filtered view. It is read-only by default, with scheduled delivery only after user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts hotspot.api4claw.com to retrieve latest hotspot data.

Mitigation: Install only when outbound contact to that service is acceptable; leave the skill in its default read-only mode unless scheduled delivery is needed.

Risk: Optional scheduled delivery depends on a user-reviewed cron command.

Mitigation: Inspect the generated command before execution and ensure destination values such as channel and recipient are trusted and free of unexpected characters.

Risk: External news data may be unavailable, malformed, or incomplete.

Mitigation: Report API, timeout, HTTP, and JSON format failures clearly, skip malformed items safely, and do not fabricate content when the service is unreachable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xltang/skills/xwzb)
- [Hotspot API base URL](https://hotspot.api4claw.com)
- [Hotspot latest endpoint](https://hotspot.api4claw.com/hotspots/latest?timestamp=$TIME_STEMP)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown responses with optional bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Top items are capped at 10; scheduled setup is optional and user-approved.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
