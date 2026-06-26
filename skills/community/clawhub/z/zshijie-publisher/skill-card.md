## Description: <br>
Operate the Zshijie publishing API from OpenClaw by guiding QR-code login and publishing or editing article and short-video content through bundled HTTP workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jkbwfi](https://clawhub.ai/user/jkbwfi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External publishers and developers use this skill to log in to Zshijie with a QR code, prepare JSON payloads, and publish or edit article and short-video content through the platform API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a reusable login session that can authorize later publishing actions. <br>
Mitigation: Treat the session file like a password, keep it out of shared workspaces, and delete or rotate it when publishing work is complete. <br>
Risk: Publish and edit commands can modify live Zshijie account content. <br>
Mitigation: Review the account, JSON payload, article_id, media URLs, and operation name before each publish or edit command. <br>
Risk: A non-default publish host could send session-bearing requests to an unintended service. <br>
Mitigation: Use the bundled host by default and only pass --base-url for a host the user explicitly trusts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jkbwfi/zshijie-publisher) <br>
- [Usage Guide](references/usage.md) <br>
- [Zshijie API Notes](references/zshijie-api.md) <br>
- [Zshijie API Contract](references/zshijie-api.json) <br>
- [Zshijie Creator Login Page](https://mp.cztv.com/#/login) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request/response payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate QR login HTML and PNG files, local session JSON, and optional saved JSON responses when commands are run.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
