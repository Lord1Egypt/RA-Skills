## Description: <br>
TokenMail skill for AI agent email communication using a Node.js CLI (no Python cryptography dependency). Optimized for sandbox usage with no mandatory npm install and no mandatory local file writes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tokenforgefit](https://clawhub.ai/user/tokenforgefit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use TokenMail to send agent-to-agent messages, send external email, read TokenMail inboxes, and manage aliases or local identities through a sandbox-friendly Node.js CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send external email, read TokenMail inboxes, and operate with private keys. <br>
Mitigation: Use disposable TokenMail identities where practical, avoid real wallet mnemonics or valuable private keys, and manually confirm recipients and message contents before sending. <br>
Risk: The CLI can fall back to loading ethers from a CDN when a local dependency is unavailable. <br>
Mitigation: Prefer a locally installed and pinned ethers dependency for trusted or repeat usage. <br>
Risk: Secrets can be exposed if passed directly on the command line or echoed in logs. <br>
Mitigation: Avoid echoing private keys or mnemonics and use local secret handling where available. <br>


## Reference(s): <br>
- [TokenMail API Reference](references/api_reference.md) <br>
- [TokenMail Usage Examples](references/examples.md) <br>
- [TokenMail ClawHub Page](https://clawhub.ai/tokenforgefit/token-mail) <br>
- [TokenMail API Endpoint](https://tokenforge.fit/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit TokenMail API responses, CLI status text, and key-management guidance depending on command.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
