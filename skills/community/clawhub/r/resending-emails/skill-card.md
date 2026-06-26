## Description: <br>
Helps agents operate Resend through the official CLI for installation, authentication, email sending, domains, webhooks, inbound mail, contacts, broadcasts, templates, profiles, and diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tristanmanchester](https://clawhub.ai/user/tristanmanchester) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to plan and execute Resend CLI workflows for live email and account operations, with guidance for deterministic subprocess use, verification, and fallback when the CLI does not cover a task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands can perform real email sends or account mutations in a live Resend account. <br>
Mitigation: Use a test or staging profile first, prefer scoped API keys and explicit profiles, and review every send, delete, update, broadcast, and API-key command before execution. <br>
Risk: Message bodies, attachments, webhook payloads, API keys, and signing secrets can be exposed through logs or command handling. <br>
Mitigation: Keep sensitive content out of logs, prefer environment variables or stored profiles over command-line secrets, and avoid pipe-to-shell installs in sensitive CI. <br>
Risk: Known CLI coverage gaps and output quirks can cause incorrect automation if an agent assumes every Resend workflow is fully covered by the CLI. <br>
Mitigation: Run diagnostic checks early, parse both stdout and stderr for JSON responses, inspect local CLI help for gap-prone flows, and fall back to MCP or API only when the CLI surface is unavailable or incomplete. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tristanmanchester/resending-emails) <br>
- [Agent operating model](references/agent-operating-model.md) <br>
- [Command selection](references/command-selection.md) <br>
- [Diagnostics and fallbacks](references/diagnostics-and-fallbacks.md) <br>
- [Sources and refresh notes](references/sources.md) <br>
- [Coverage gaps](assets/coverage-gaps.json) <br>
- [Resend CLI changelog](https://resend.com/changelog/cli) <br>
- [Official Resend CLI repository](https://github.com/resend/resend-cli) <br>
- [Resend API documentation](https://resend.com/docs/api-reference/introduction) <br>
- [Resend webhook verification](https://resend.com/docs/webhooks/verify-webhooks-requests) <br>
- [Resend MCP server](https://resend.com/docs/mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, code snippets, JSON examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include verification steps, generated file scaffolds, diagnostic interpretations, and fallback paths for unsupported CLI flows.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; source skill metadata reports 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
