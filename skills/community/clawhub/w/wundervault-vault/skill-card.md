## Description: <br>
Read passwords, API keys, and credentials from a Wundervault zero-knowledge, multi-agent vault, and run authorized shell commands with secrets injected without exposing them in chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snoweman](https://clawhub.ai/user/snoweman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect an agent to Wundervault, list permitted vault entries, run authorized commands with scoped secrets injected, and write secrets to approved config files without exposing plaintext in chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables an agent to use scoped vault credentials for commands, configuration files, SSH, and deployment tasks. <br>
Mitigation: Install only when that access is intended, verify the npm package and onboarding script checksum or signature before setup, and keep vault grants least-privilege. <br>
Risk: Environment-file injection can place secrets on disk where they persist outside burn-on-read vault workflows. <br>
Mitigation: Enable .env injection only for workflows where the impact is understood, review target paths, and manage file permissions for written secret files. <br>
Risk: Tier 2 secrets and deployment actions can affect production systems if granted too broadly. <br>
Mitigation: Use server-side Tier 2 enablement only for approved workflows and limit each agent to the entries required for its task. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/snoweman/wundervault-vault) <br>
- [Wundervault](https://wundervault.com) <br>
- [Wundervault Install Verification](https://wundervault.com/install) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline tool-call examples, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide MCP tool calls that inject vaulted credentials without returning plaintext secrets.] <br>

## Skill Version(s): <br>
1.6.3 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
