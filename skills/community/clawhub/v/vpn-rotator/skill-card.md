## Description: <br>
Vpn Rotator guides agents in configuring and managing VPN rotation workflows with multi-VPN pools, load balancing, auto-reconnect, circuit breaking, region routing, and monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data engineering teams, automation testing teams, and security testing teams use this skill to produce VPN rotation guidance, configuration, code patterns, and command-oriented setup steps for multi-provider VPN workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests powerful local and system access for VPN route changes, OpenVPN commands, and related automation. <br>
Mitigation: Use it only in a controlled environment, require explicit user confirmation before route or VPN changes, and narrow exec/write authority to audited VPN-only operations. <br>
Risk: VPN credentials and configuration files may be stored or manipulated by generated workflows. <br>
Mitigation: Use a secret manager or locked-down files, keep credential files out of repositories, and enforce restrictive permissions such as 600 for local credential files. <br>
Risk: Passwordless sudo or broad command execution can expand the impact of mistakes in generated VPN automation. <br>
Mitigation: Do not grant passwordless sudo unless the command allowlist has been audited and constrained to the minimum OpenVPN operations needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/vpn-rotator) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON examples, Python snippets, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include OpenVPN setup steps, credential handling guidance, and executable command suggestions that require review before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
