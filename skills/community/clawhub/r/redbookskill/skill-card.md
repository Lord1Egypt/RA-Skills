## Description:

Collects Xiaohongshu fruit tea, coffee, and health drink low-follower viral trends from the last 24 hours, generates a mobile-friendly HTML topic report, and sends it to a Feishu group daily at 9:00.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuheng0330](https://clawhub.ai/user/yuheng0330)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators and social media operators use this skill to automate daily Xiaohongshu beverage topic research, filter out brand-led posts, and receive reusable topic ideas in Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trend summaries, links, and report attachments are sent to the configured Feishu webhook on the schedule.

Mitigation: Confirm the webhook points to a private intended group before installation and keep Feishu bot security settings enabled.

Risk: Report reference links may be unsafe or outside the expected Xiaohongshu source domain.

Mitigation: Treat report links as untrusted unless the workflow validates them to expected HTTPS Xiaohongshu domains.

Risk: Automated topic recommendations may not be sufficient for compliant or original published content.

Mitigation: Review generated topics before publishing and add personal footage, original perspective, and platform-appropriate judgment.

## Reference(s):

- [Artifact README](artifact/README.md)
- [Skill Instructions](artifact/SKILL.md)
- [Report Template](artifact/assets/report_template.html)
- [Volcengine](https://www.volcengine.com/)

## Skill Output:

**Output Type(s):** [Text, HTML, Configuration, Guidance]

**Output Format:** [Mobile-friendly HTML report with Feishu message preview and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-configured FEISHU_WEBHOOK and scheduled execution settings.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
