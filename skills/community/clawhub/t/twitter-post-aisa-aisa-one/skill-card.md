## Description: <br>
Run Twitter/X read context, approved likes, follows, replies, and OAuth-gated posting through AIsa. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to run explicit Twitter/X engagement and posting workflows when the target account, tweet, campaign, or content has already been chosen and approved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AISA_API_KEY may be exposed in posting or authorization output if scripts print or return credentials. <br>
Mitigation: Inspect or patch scripts before authorization or posting, use a scoped and revocable key, and avoid running the skill where terminal output is logged or shared. <br>
Risk: The skill can post, reply, like, follow, unfollow, and upload media to Twitter/X through AIsa. <br>
Mitigation: Require explicit user approval for external actions, verify relay responses before reporting success, and upload only local files the user attached. <br>
Risk: Twitter/X queries, account actions, and uploaded media are sent to AIsa's API endpoint. <br>
Mitigation: Install only if you trust AIsa with that data, and provide only AISA_API_KEY rather than passwords, cookies, or browser credential exports. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/aisadocs/twitter-post-aisa-aisa-one) <br>
- [AIsa Twitter Engagement](references/engage_twitter.md) <br>
- [AIsa Twitter OAuth](references/post_twitter.md) <br>
- [AIsa homepage](https://aisa.one) <br>
- [AIsa Twitter API endpoint](https://api.aisa.one/apis/v1/twitter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON responses from bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and user approval for posting, engagement actions, and media uploads.] <br>

## Skill Version(s): <br>
1.0.3 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
