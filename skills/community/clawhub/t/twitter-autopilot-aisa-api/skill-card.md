## Description: <br>
Reads and searches X (Twitter) data including profiles, timelines, mentions, followers, tweet search, trends, lists, communities, and Spaces, and supports posting, liking, unliking, following, and unfollowing after OAuth authorization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill for Twitter/X research, social listening, trend monitoring, publishing, and authorized account engagement without sharing account passwords. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured AISA_API_KEY may appear in normal command output or logs. <br>
Mitigation: Use a dedicated key that can be rotated, and avoid sharing logs or transcripts from status, authorize, or post commands. <br>
Risk: Posting, liking, following, or unfollowing can create visible public account activity. <br>
Mitigation: Confirm every publish and engagement action with the user before execution and do not report success until the relay returns success. <br>
Risk: Files passed with --media-file are uploaded to AIsa's relay and Twitter/X. <br>
Mitigation: Treat each media path as an external upload and verify the file selection before running media-post commands. <br>


## Reference(s): <br>
- [Twitter Autopilot Release Page](https://clawhub.ai/bibaofeng/twitter-autopilot-aisa-api) <br>
- [Twitter Autopilot README](README.md) <br>
- [Twitter OAuth Workflow](references/post_twitter.md) <br>
- [Twitter Engagement Workflow](references/engage_twitter.md) <br>
- [AIsa API Reference](https://aisa.one/docs/api-reference/) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY; optional TWITTER_RELAY_BASE_URL and TWITTER_RELAY_TIMEOUT configure relay behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
