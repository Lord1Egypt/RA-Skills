## Description: <br>
Connect 8,000+ apps via Zapier MCP. Includes full UI integration for Clawdbot Gateway dashboard. Use when setting up Zapier integration, connecting apps, or using Zapier tools via mcporter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to connect a Clawdbot environment to Zapier MCP, configure a personal MCP URL, inspect available Zapier tools, and call those tools through mcporter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Zapier MCP URL functions as a secret and can authorize actions across connected apps. <br>
Mitigation: Treat the URL like a password, keep it out of shared logs or screenshots, and regenerate it in Zapier if exposure is suspected. <br>
Risk: Zapier actions can send messages, spend money, or modify business data depending on which actions are exposed. <br>
Mitigation: Limit exposed actions in Zapier and require confirmation before high-impact operations. <br>
Risk: Loose endpoint validation may accept any HTTPS URL during setup. <br>
Mitigation: Verify the MCP URL begins with the official Zapier MCP domain before saving it. <br>


## Reference(s): <br>
- [Zapier MCP release page](https://clawhub.ai/maverick-software/zapier-mcp) <br>
- [Zapier MCP](https://zapier.com/mcp) <br>
- [Zapier Help](https://help.zapier.com) <br>
- [Zapier MCP reference files](artifact/reference/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell command examples and TypeScript reference code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter and Clawdbot Gateway v2026.1.0 or later.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
