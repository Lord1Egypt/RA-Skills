## Description:

Creates a Zhihu article from a user-provided topic, presents the draft for confirmation, then uses browser or API automation to publish it to the user's Zhihu account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelcey2023](https://clawhub.ai/user/kelcey2023)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content operators use this skill to research a topic, draft a structured Zhihu article, review it, and publish only after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish content to a live Zhihu account.

Mitigation: Review the full article before confirming publication, and do not approve publishing unless the draft is ready to post.

Risk: Browser or API publishing can target the wrong destination if environment overrides are set or Browser Relay is attached to the wrong tab.

Mitigation: Avoid setting ZHIHU_API_BASE or ZHIHU_BASE, and attach Browser Relay only to the real Zhihu editor tab.

Risk: API mode uses a Zhihu access token.

Mitigation: Use a narrowly scoped, short-lived Zhihu token when API publishing is enabled.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kelcey2023/skills/zeelin-zhihu-autopost)
- [Zhihu Open Platform](https://dev.zhihu.com/)
- [Zhihu Article API Endpoint](https://api.zhihu.com/v4/articles)
- [OpenClaw Browser Relay Documentation](https://learnclawdbot.org/docs/tools/chrome-extension)
- [Referenced ClawHub Zhihu Posting Skill](https://clawhub.ai/InuyashaYang/zhihu-post)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, API Calls, Guidance]

**Output Format:** [Markdown draft text with shell commands or API/browser publishing actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Publishes only after user confirmation; browser mode depends on an authenticated Zhihu editor tab and OpenClaw Browser Relay.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
