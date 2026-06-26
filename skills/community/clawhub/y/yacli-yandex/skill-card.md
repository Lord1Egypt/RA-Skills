## Description: <br>
Connects OpenClaw agents to a configured yacli MCP server for Yandex Mail, Disk, and Calendar workflows, including mail triage, file sharing, and calendar lookup or scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qoderone](https://clawhub.ai/user/qoderone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to operate Yandex Mail, Disk, and Calendar through a trusted local yacli MCP server. It supports account discovery, email read and reply flows, Disk upload and sharing, and calendar lookup or scheduling with explicit approval for externally visible actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to send email, publish files, or create and delete calendar events through the configured Yandex account. <br>
Mitigation: Require explicit user approval for recipients, message content, file visibility, and calendar IDs before any write, publish, send, create, or delete action. <br>
Risk: A misconfigured or untrusted yacli MCP server could expose account data or execute actions against the wrong account. <br>
Mitigation: Verify that mcporter points to a trusted yacli-mcp-server and check account and authentication status before use. <br>
Risk: Local Yandex tokens or account snapshots could be exposed if configuration directories or generated logs are published or left unprotected. <br>
Mitigation: Protect the yacli configuration directory and do not publish real tokens, cookies, account snapshots, or logs containing personal data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/qoderone/yacli-yandex) <br>
- [yacli upstream project](https://github.com/NextStat/yacli) <br>
- [Installation](references/install.md) <br>
- [Example mcporter wiring](references/mcporter-config.md) <br>
- [yacli Yandex Setup](references/setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown with inline shell commands, MCP tool names, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct the agent to call yacli MCP tools that read or modify mail, files, and calendar events after user approval.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
