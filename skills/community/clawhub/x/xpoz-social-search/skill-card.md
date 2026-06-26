## Description: <br>
Search Twitter, Instagram, and Reddit posts in real time to find social media mentions, track hashtags, discover influencers, and analyze engagement across Xpoz's indexed social data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atyachin](https://clawhub.ai/user/atyachin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and users doing social listening, brand monitoring, competitor research, influencer discovery, or community discovery use this skill to run Xpoz MCP searches across Twitter, Instagram, and Reddit. It supports post, profile, user, and subreddit lookup workflows with polling for asynchronous results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, result polling, and exports are handled by Xpoz's external service. <br>
Mitigation: Use only with queries and data that your organization approves for submission to Xpoz. <br>
Risk: The skill depends on mcporter, xpoz-setup, an Xpoz account, and network access to mcp.xpoz.ai. <br>
Mitigation: Confirm these dependencies and access requirements before deployment. <br>
Risk: Search operations return operation IDs before results are available. <br>
Mitigation: Poll checkOperationStatus before relying on returned results or export URLs. <br>


## Reference(s): <br>
- [Xpoz](https://xpoz.ai) <br>
- [xpoz-setup skill](https://clawhub.ai/skills/xpoz-setup) <br>
- [ClawHub listing](https://clawhub.ai/atyachin/xpoz-social-search) <br>
- [Publisher profile](https://clawhub.ai/user/atyachin) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides agents to call Xpoz MCP tools, poll operation status, and request CSV exports when available.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
