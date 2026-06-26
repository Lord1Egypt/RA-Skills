## Description: <br>
TopYappers provides social media intelligence for agents to discover viral TikTok content, search creators across TikTok, Instagram, and YouTube, and track trending song charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tadasgedgaudas](https://clawhub.ai/user/tadasgedgaudas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and social media teams use this skill to connect agents to TopYappers MCP workflows for creator discovery, viral content research, video search, and trending song analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TopYappers API keys and account credits can be exposed or misused if shared broadly. <br>
Mitigation: Use a scoped or revocable API key, store it outside prompts and checked-in files, and monitor credit usage. <br>
Risk: Search terms may disclose confidential campaign plans or personal data to an external service. <br>
Mitigation: Avoid sending confidential plans, private identifiers, or sensitive personal data as search queries. <br>
Risk: Creator emails returned by profile tools are sensitive contact data. <br>
Mitigation: Handle creator emails according to consent, anti-spam, platform, and privacy obligations. <br>


## Reference(s): <br>
- [TopYappers Platform](https://www.topyappers.com) <br>
- [TopYappers API Documentation](https://docs.topyappers.com) <br>
- [TopYappers MCP Documentation](https://www.topyappers.com/tools/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with shell commands, JSON configuration examples, and API workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a TopYappers API key and may consume TopYappers credits depending on the selected MCP tool.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
