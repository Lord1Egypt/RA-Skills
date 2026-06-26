## Description: <br>
Searches Reddit posts, comments, users, and subreddits through Xpoz MCP using natural language and boolean queries without requiring a Reddit API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atyachin](https://clawhub.ai/user/atyachin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, researchers, analysts, and developers use this skill to search Reddit discussions, discover communities and users, inspect post and comment history, and export search results through Xpoz MCP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Reddit searches and exports through Xpoz infrastructure. <br>
Mitigation: Avoid confidential or regulated queries unless Xpoz's controls are approved for that data. <br>
Risk: CSV export URLs may expose externally hosted search results. <br>
Mitigation: Treat export links as sensitive and share or store them only according to the user's data handling requirements. <br>
Risk: The skill depends on the mcporter npm package and an authenticated Xpoz account. <br>
Mitigation: Install mcporter from a trusted package source and authorize only the intended Xpoz account before use. <br>


## Reference(s): <br>
- [Reddit Search on ClawHub](https://clawhub.ai/atyachin/reddit-api) <br>
- [Xpoz](https://xpoz.ai) <br>
- [xpoz-setup Skill](https://clawhub.ai/skills/xpoz-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and API call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter, xpoz-setup, network access to mcp.xpoz.ai, and an Xpoz account; CSV exports can return externally hosted download URLs.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
