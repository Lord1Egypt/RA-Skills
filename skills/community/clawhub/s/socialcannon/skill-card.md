## Description: <br>
Publish, schedule, and manage social media posts across Twitter/X, Facebook, Instagram, LinkedIn, TikTok, and YouTube with calendar analysis, A/B testing, engagement inbox workflows, content repurposing, timing suggestions, auto-scheduling, and UTM tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miprinia](https://clawhub.ai/user/miprinia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to operate SocialCannon's social publishing API, including account setup, posting, scheduling, analytics, engagement replies, media uploads, content repurposing, and platform-specific publishing constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide actions that publish posts, replies, or repurposed content to connected social accounts. <br>
Mitigation: Require explicit user approval and review final content, target account, platform options, and schedule before any publishing or public reply action. <br>
Risk: The skill uses SocialCannon client secrets and bearer tokens for account-level API access. <br>
Mitigation: Keep client secrets and bearer tokens out of prompts, logs, and shared transcripts; rotate credentials if exposure is suspected. <br>
Risk: Account disconnect and post deletion endpoints can remove integrations or published content. <br>
Mitigation: Confirm the specific account or post identifier and the intended irreversible effect before disconnecting accounts or deleting posts. <br>
Risk: Platform-specific constraints can cause failed or non-compliant posts, especially for TikTok privacy settings and media requirements. <br>
Mitigation: Check platform capabilities and validation responses before posting; for TikTok, fetch creator info and choose an allowed privacy level before submitting. <br>


## Reference(s): <br>
- [SocialCannon homepage](https://socialcannon.app) <br>
- [@socialcannon/mcp package](https://www.npmjs.com/package/@socialcannon/mcp) <br>
- [ClawHub Socialcannon skill page](https://clawhub.ai/miprinia/skills/socialcannon) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown with curl commands, JSON request and response examples, and MCP configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SocialCannon client credentials and connected social accounts; some workflows can publish, reply publicly, disconnect accounts, or delete posts.] <br>

## Skill Version(s): <br>
1.8.3 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
