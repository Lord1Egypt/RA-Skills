## Description: <br>
LDM OS installer and updater for installing, updating, and checking the status of local LDM OS environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks) <br>

### License/Terms of Use: <br>
Dual License: MIT + AGPLv3 <br>


## Use Case: <br>
Developers and external users use this skill to guide an agent through checking whether LDM OS is installed, reviewing a dry run, installing or updating the CLI, and validating the local setup. It is intended for local AI infrastructure management across agent tools such as Claude Code, GPT-compatible workflows, and OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make broad persistent changes to local AI tooling, hooks, MCP registrations, OpenClaw allowlists, background behavior, and files under ~/.ldm, ~/.claude, and ~/.openclaw. <br>
Mitigation: Review the dry run before installation, confirm the exact files and registrations that will change, and install only on machines where LDM OS should manage the local AI environment. <br>
Risk: This version can persist OP_SERVICE_ACCOUNT_TOKEN into the user's shell profile when 1Password service-account workflows are enabled. <br>
Mitigation: Avoid enabling 1Password service-account token flows on sensitive machines unless the credential storage behavior has been reviewed and accepted. <br>
Risk: The server security verdict is suspicious because the package has capabilities involving wallets, purchases, OAuth or sensitive credentials, and external posting. <br>
Mitigation: Treat credential, payment, and posting workflows as privileged actions and require explicit user confirmation before running commands that enable or configure them. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/parkertoddbrooks/wip-ldm-os) <br>
- [Publisher Profile](https://clawhub.ai/user/parkertoddbrooks) <br>
- [Project Homepage](https://github.com/wipcomputer/wip-ldm-os) <br>
- [Install Prompt](https://wip.computer/install/wip-ldm-os.txt) <br>
- [Product Overview](references/PRODUCT.md) <br>
- [Command Reference](references/COMMANDS.md) <br>
- [Interface Reference](references/INTERFACES.md) <br>
- [Skills Catalog](references/SKILLS-CATALOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and status tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides dry-run-first installation and update workflows; may produce commands that modify local LDM OS, Claude Code, OpenClaw, MCP, hook, and shell-profile configuration after user approval.] <br>

## Skill Version(s): <br>
0.4.84 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
