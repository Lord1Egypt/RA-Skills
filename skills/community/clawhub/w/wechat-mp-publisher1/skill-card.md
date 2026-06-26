## Description: <br>
Remote WeChat Official Account publishing skill that routes Markdown article publishing through an HTTP MCP service, with credential isolation and dependency checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cp33333333333](https://clawhub.ai/user/cp33333333333) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to publish Markdown articles to WeChat Official Account drafts from an agent workflow or shell script. It is aimed at users who need remote MCP publishing when local IP whitelist constraints make direct WeChat API access unreliable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing through a remote MCP endpoint can send full article drafts and live WeChat credentials outside the local environment. <br>
Mitigation: Use only trusted, controlled MCP endpoints, prefer HTTPS, and confirm the endpoint configuration before publishing. <br>
Risk: WeChat AppID and AppSecret values are sensitive long-lived account secrets. <br>
Mitigation: Keep wechat.env and any TOOLS.md credentials out of version control and restrict local file access. <br>
Risk: The skill can publish or upload article content and images to a WeChat draft workflow. <br>
Mitigation: Review the exact Markdown article, frontmatter, cover image, and media references before running publish scripts or asking an agent to publish. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cp33333333333/wechat-mp-publisher1) <br>
- [SKILL.md](SKILL.md) <br>
- [README.md](README.md) <br>
- [Theme reference](references/themes.md) <br>
- [Troubleshooting guide](references/troubleshooting.md) <br>
- [wenyan-mcp](https://github.com/caol64/wenyan-mcp) <br>
- [wenyan-cli](https://github.com/caol64/wenyan-cli) <br>
- [wenyan-core themes](https://github.com/caol64/wenyan-core/tree/main/src/assets/themes) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May transmit article content and WeChat credentials to a configured remote MCP endpoint during publishing.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 2.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
