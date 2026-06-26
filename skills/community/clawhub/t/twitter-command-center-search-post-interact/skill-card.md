## Description: <br>
Search X/Twitter profiles, tweets, trends, and OAuth-gated posting through AIsa for research, monitoring, and approved engagement workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to research Twitter/X accounts, tweets, trends, lists, communities, and Spaces, then perform OAuth-gated posting or engagement actions after approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured AISA_API_KEY may appear in normal command output. <br>
Mitigation: Run commands only in private terminals or traces, keep the key out of logs, and rotate the key if it is exposed. <br>
Risk: The skill can perform real Twitter/X posting, liking, unliking, following, unfollowing, and media upload actions. <br>
Mitigation: Require explicit user approval immediately before any external account action and confirm success only from the relay response. <br>
Risk: The skill delegates Twitter/X account actions to AIsa/api.aisa.one. <br>
Mitigation: Install and run it only when the user trusts that service with the intended account actions and OAuth flow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bibaofeng/twitter-command-center-search-post-interact) <br>
- [Twitter Engagement](references/engage_twitter.md) <br>
- [Twitter OAuth](references/post_twitter.md) <br>
- [AIsa Twitter API Endpoint](https://api.aisa.one/apis/v1/twitter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and may return authorization links, tweet IDs, tweet links, or relay status payloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
