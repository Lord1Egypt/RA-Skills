## Description: <br>
Social By IDM helps agents create, schedule, publish, update, delete, and analyze social media posts across Instagram, Facebook, X/Twitter, LinkedIn, and TikTok through the Social by InstantDM API and hosted MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sanjaykhanssk](https://clawhub.ai/user/sanjaykhanssk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, social media operators, and developers use this skill to connect agents to Social by InstantDM for drafting, scheduling, cross-posting, publishing, deleting, status checks, and analytics across connected social accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish, schedule, edit, and delete posts on connected social accounts through the service API. <br>
Mitigation: Use scoped API keys, prefer draft mode for review, and confirm before publishing live content. <br>
Risk: An exposed workspace API key could allow unauthorized actions against connected social accounts. <br>
Mitigation: Store the key like a password, do not search local secret stores for it, and revoke the key from the dashboard when access is no longer needed. <br>
Risk: Platform-specific delete, status, and publishing behavior can produce partial results or leave content live. <br>
Mitigation: Check per-platform status, inspect delete results, and verify important changes against the real social feed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sanjaykhanssk/skills/social-by-idm) <br>
- [Server-resolved GitHub source](https://github.com/sanjaykhanssk/social-by-idm/tree/main/skills/social-by-idm) <br>
- [Social by InstantDM API documentation](https://socialbyidm.com/docs) <br>
- [Social by InstantDM MCP server](https://socialbyidm.com/mcp) <br>
- [Social by InstantDM agents overview](https://socialbyidm.com/agents) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API calls, JSON examples] <br>
**Output Format:** [Markdown with JSON configuration and REST request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Social by InstantDM workspace API key; recommends draft mode and explicit confirmation before live publishing.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
