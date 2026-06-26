## Description: <br>
Automates guided setup of a VLESS+Reality proxy using sing-box on a VPS, including SSH-based server deployment, Clash Verge client configuration, and connectivity checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1126misakp](https://clawhub.ai/user/1126misakp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technically capable users use this skill to configure and validate a VPS-hosted proxy for access through a VLESS+Reality tunnel. The skill guides setup, deployment, client configuration, acceptance testing, and later troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles plaintext SSH, VPS, and proxy credentials in local files. <br>
Mitigation: Keep proxy-setup-info.txt and .proxy-keys.txt out of synced folders, shared workspaces, backups, and repositories; rotate credentials if either file is exposed. <br>
Risk: The skill makes persistent changes to a remote VPS over SSH. <br>
Mitigation: Use a dedicated non-production VPS, verify the server fingerprint yourself, and review commands before execution. <br>
Risk: The skill can modify its own installed troubleshooting reference files. <br>
Mitigation: Monitor installed reference files for unexpected changes and review the skill before reuse after troubleshooting sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1126misakp/proxy-expert) <br>
- [README](README.md) <br>
- [Server configuration templates](references/server-configs.md) <br>
- [Client configuration template](references/client-config.md) <br>
- [Troubleshooting guide](references/troubleshooting.md) <br>
- [sing-box documentation](https://sing-box.sagernet.org) <br>
- [Clash Verge Rev install page](https://clashvergerev.com/install) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local setup, key, client configuration, and acceptance-report files during use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
