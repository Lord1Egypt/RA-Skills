## Description: <br>
Tencent News helps agents retrieve and present 24/7 news, rankings, briefings, real-time updates, domain news, and weather information from Tencent News. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencentnewsteam](https://clawhub.ai/user/tencentnewsteam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search Tencent News content, check hot topics, retrieve morning or evening briefings, follow domain-specific news, and query weather-related information. It is intended for environments where the Tencent News CLI is installed and a Tencent News API key is configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation and fallback update paths can run hosted scripts that execute with the user's privileges. <br>
Mitigation: Only install from the TencentNews publisher if trusted; download and inspect the installer first, and verify a publisher-provided checksum or signature when available. <br>
Risk: The skill requires managing a Tencent News API key on the local machine. <br>
Mitigation: Use the provided API key commands for setup and clearing, avoid sharing the key in prompts or logs, and remove it when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tencentnewsteam/tencent-news) <br>
- [API Key Configuration Guide](references/env-setup-guide.md) <br>
- [Manual Installation Guide](references/installation-guide.md) <br>
- [Manual Update Guide](references/update-guide.md) <br>
- [Tencent News API Key Page](https://news.qq.com/exchange?scene=appkey) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown news summaries with links and inline shell commands for setup or troubleshooting] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require a configured Tencent News API key and local Tencent News CLI before news retrieval succeeds.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
