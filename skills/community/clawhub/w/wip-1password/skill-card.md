## Description: <br>
Headless plugin for 1Password secrets using service accounts, resolving op:// references, reading/writing secrets, and listing vault items via JS SDK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to let Claude Code, OpenClaw, or MCP-compatible agents retrieve, list, and optionally write 1Password secrets through a service account. It is intended for replacing pasted credentials and plaintext config values with runtime vault access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent direct access to read 1Password secrets. <br>
Mitigation: Use a least-privilege service account scoped to a dedicated vault and avoid exposing secret values in chat, logs, shell history, or shared files. <br>
Risk: Write access can let an agent create or modify credentials. <br>
Mitigation: Do not grant write_items unless agent-managed secrets are required, and review every write request before allowing it. <br>
Risk: Untrusted prompts or workflows could attempt to misuse the MCP server or secret tooling. <br>
Mitigation: Do not expose this MCP server to untrusted prompts or workflows until command construction and authorization controls are tightened. <br>
Risk: A leaked 1Password service account token can compromise the scoped vault. <br>
Mitigation: Treat the local ops_ token as a production credential and rotate it immediately if it appears in logs, shell history, or shared files. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/parkertoddbrooks/wip-1password) <br>
- [README](README.md) <br>
- [Technical documentation](TECHNICAL.md) <br>
- [Setup guide](docs/SETUP.md) <br>
- [Skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include redacted secret previews and configuration snippets; secret values should not be exposed in chat, logs, or files.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
