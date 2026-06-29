## Description: <br>
Provides a Weibo data assistant for hot searches, post research, post details, comment analysis, replies, engagement review, creator profiles, and creator post lists through SocialDataX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve and analyze Weibo hot-search, post, comment, engagement, and creator data with a SocialDataX API key. It supports read-only research workflows through direct CLI commands or matching MCP tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses SOCIALDATAX_API_KEY and sends Weibo research queries to the SocialDataX service. <br>
Mitigation: Install only when SocialDataX is trusted, scope and protect the API key, and avoid sending sensitive queries unless the service is approved for that data. <br>
Risk: The documented direct CLI uses socialdatax-skills@latest, so behavior can change when the npm package changes. <br>
Mitigation: Pin and review a specific package version before deployment when repeatability or change control is required. <br>


## Reference(s): <br>
- [SocialDataX homepage](https://socialdatax.com/?from=clawhub) <br>
- [ClawHub skill page](https://clawhub.ai/devinchen2014/skills/socialdatax-weibo) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/devinchen2014) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and tool guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SOCIALDATAX_API_KEY, node, and npm; data access is read-only.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
