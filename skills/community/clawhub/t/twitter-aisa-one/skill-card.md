## Description: <br>
Searches and reads X/Twitter profiles, timelines, mentions, followers, tweet search, trends, lists, communities, and Spaces, and can post, like, unlike, follow, and unfollow after browser OAuth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baofeng-tech](https://clawhub.ai/user/baofeng-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill for Twitter/X data lookup, social listening, trend monitoring, posting, and account engagement through the AIsa service. It is suited to workflows that need API-key-backed Twitter/X access without sharing the user's account password. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose the configured AIsa API key in normal command output. <br>
Mitigation: Avoid running status or authorization commands in shared logs and review outputs for credential leakage until key redaction is fixed. <br>
Risk: The skill can perform real Twitter/X account-changing actions, including posts, likes, follows, unfollows, and media uploads. <br>
Mitigation: Require explicit user review and confirmation before executing posting, engagement, or media upload workflows. <br>
Risk: Twitter/X activity, post content, uploaded media, and the AIsa API key are handled by the AIsa service. <br>
Mitigation: Install and use the skill only when the user trusts AIsa for the relevant Twitter/X activity and credentials. <br>


## Reference(s): <br>
- [ClawHub Twitter skill page](https://clawhub.ai/baofeng-tech/twitter-aisa-one) <br>
- [AIsa](https://aisa.one) <br>
- [AIsa API Reference](https://docs.aisa.one/reference/) <br>
- [AIsa Twitter Engagement](references/engage_twitter.md) <br>
- [AIsa Twitter OAuth](references/post_twitter.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown and plain text with Python command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY; OAuth is required before posting or account engagement actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
