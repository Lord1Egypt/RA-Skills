## Description: <br>
OpenClaw Video Publisher helps agents publish, schedule, retry, and track video uploads across Douyin, Kuaishou, WeChat Channels, Bilibili, YouTube, TikTok, and related short-video platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZhenStaff](https://clawhub.ai/user/ZhenStaff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, content teams, and agent builders use this skill to automate multi-platform video publishing workflows, including credential setup, batch upload commands, scheduling, retry behavior, and publication history checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent could publish, schedule, retry, or batch-upload public posts to linked accounts without adequate human approval. <br>
Mitigation: Require explicit user confirmation before every upload, batch publish, retry, or scheduled post; use review queues or dry runs before enabling live publishing. <br>
Risk: Platform credentials could expose creator or business accounts if broad production tokens are used too early. <br>
Mitigation: Start with test or least-privilege credentials, keep secrets in environment-managed stores, avoid logging full credentials, and rotate tokens after validation. <br>
Risk: Bulk publishing can hit platform rate limits or create inconsistent publishing state across services. <br>
Mitigation: Throttle batch jobs, monitor platform quotas and publish-history records, and use bounded retry behavior with operator review for repeated failures. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ZhenStaff/video-publisher) <br>
- [npm package listed in artifact documentation](https://www.npmjs.com/package/openclaw-video-publisher) <br>
- [Project repository listed in artifact documentation](https://github.com/ZhenRobotics/openclaw-video-publisher) <br>
- [YouTube Data API v3](https://console.cloud.google.com/) <br>
- [TikTok for Developers](https://developers.tiktok.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell, JSON, and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance includes platform credential configuration, batch publishing examples, retry settings, scheduling, and publish-history review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
