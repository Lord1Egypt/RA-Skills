## Description:

Install 3x-ui panels on servers via SSH and create VLESS+Reality+TCP nodes with SOCKS5 outbound binding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[n0vemb](https://clawhub.ai/user/n0vemb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install 3x-ui panels, register panel access, create VLESS nodes, bind SOCKS5 outbound routing, and return connection artifacts to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated remote administration can change servers without strong trust checks.

Mitigation: Review planned actions before execution and use disposable or test servers unless the operator accepts the automation risk.

Risk: SSH, panel, and SOCKS5 credentials can be exposed through chat, command arguments, or plaintext YAML configuration.

Mitigation: Avoid passing passwords in chat or command arguments and do not store panel passwords in plaintext YAML.

Risk: The installer fetches and executes a remote shell script.

Mitigation: Replace the remote curl-to-bash installer with a pinned and verified source before production use.

Risk: Weak transport trust can expose panel administration traffic or allow host impersonation.

Mitigation: Require HTTPS with valid certificates and verify SSH host keys before connecting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/n0vemb/skills/xui-node-manager)
- [3x-ui upstream installer](https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown text with shell commands, configuration edits, generated QR PNG files, and vless:// URIs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local YAML configuration and QR image files while administering remote 3x-ui panels.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
