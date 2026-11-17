## Description:

营销引流工具包：通过分析热点在微博或X上自动发文。支持热点发现、内容生成、MCP浏览器发布、效果分析。英文推文发X，中文发微博，支持主人选择发布平台。

This skill is ready for commercial/non-commercial use.

## Publisher:

[silbosu](https://clawhub.ai/user/silbosu)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers and business operators use this skill to identify trending topics, generate short promotional posts, publish to X or Weibo, and review posting performance. It supports content planning, platform selection, publishing status updates, and recurring analysis from the posting log.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended posting to real social media accounts can publish unsuitable content or harm account reputation.

Mitigation: Prefer draft-only or explicit per-post approval before public posting, especially for brand or customer-facing accounts.

Risk: Frequent automated posting can trigger platform enforcement or rate-limiting.

Mitigation: Keep posting frequency low, avoid repeated content, avoid repeating the same trend within 24 hours, and respect the artifact's pacing guidance.

Risk: Local posting logs can retain account performance and campaign details.

Mitigation: Review posts-log.md regularly and avoid recording sensitive account, audience, or campaign data unless retention is intentional.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/silbosu/skills/vdoob-marketing)
- [Publisher profile](https://clawhub.ai/user/silbosu)
- [X post composer](https://x.com/compose/post)
- [X explore trends](https://x.com/explore/tabs/trending)
- [Weibo](https://weibo.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown guidance with generated social post text, posting instructions, status notifications, and performance review notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated posts target 280 characters for X and 500 Chinese characters for Weibo; posting outcomes are recorded in posts-log.md.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
