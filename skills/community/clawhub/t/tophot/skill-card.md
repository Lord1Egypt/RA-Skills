## Description:

今日热点 fetches public trending-topic data from a fixed hotspot API and presents titles grouped by source, with optional user-approved daily scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xltang](https://clawhub.ai/user/xltang)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to retrieve current hotspot and trending-topic summaries for supported sources such as daily hotspots, Weibo, CCTV News, Zhihu, and Tencent Morning News. It can also report service status and provide an optional cron setup command after user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may suggest a daily cron job for hotspot updates.

Mitigation: Approve scheduled delivery only when recurring messages are desired; otherwise keep the default read-only mode.

Risk: Ambiguous requests containing "热点" may trigger the skill and fetch public hotspot data.

Mitigation: Use the skill for hotspot intents and rely on its fixed API endpoint scope; do not persist identifiers or create background tasks without explicit approval.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xltang/skills/tophot)
- [Hotspot API Base URL](https://hotspot.api4claw.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Concise Markdown with grouped hotspot titles and optional shell command blocks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only by default; optional scheduled delivery requires user approval.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
