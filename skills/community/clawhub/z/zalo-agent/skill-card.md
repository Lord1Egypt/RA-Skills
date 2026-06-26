## Description: <br>
Automates Zalo messaging, Official Account workflows, real-time listeners, webhooks, and MCP integration through the preinstalled zalo-agent CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PhucMPham](https://clawhub.ai/user/PhucMPham) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to have an agent prepare Zalo CLI workflows for messaging, groups, Official Accounts, webhooks, and MCP integrations. It is intended for environments where the user has already installed and authorized the zalo-agent command-line tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent operate real Zalo accounts or Official Accounts and send, forward, store, or expose private messages. <br>
Mitigation: Use it only with trusted conversations and endpoints, confirm recipients and message content before account-changing actions, and apply filters or whitelists for listeners. <br>
Risk: Exported credentials and session files can enable account takeover if copied, logged, committed, or shared. <br>
Mitigation: Treat exported credentials as secrets, keep restrictive file permissions, avoid committing them, and delete or rotate credentials when no longer needed. <br>
Risk: Webhook, MCP, or OA listener endpoints can expose account data if left unauthenticated or run with verification disabled. <br>
Mitigation: Require authentication for remote MCP endpoints, use HTTPS and verified webhook domains, and avoid no-verify modes outside local testing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PhucMPham/zalo-agent) <br>
- [Login flow](references/login-flow.md) <br>
- [Command reference](references/command-reference.md) <br>
- [Official Account command reference](references/oa-command-reference.md) <br>
- [Listen mode guide](references/listen-mode-guide.md) <br>
- [MCP guide](references/mcp-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that operate live Zalo accounts, configure webhooks or MCP endpoints, and handle credential-related setup.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
