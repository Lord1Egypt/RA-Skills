## Description: <br>
Helps agents guide developers through configuring and using OpenVPN-based VPN rotation for data collection, automated testing, price monitoring, and SEO rank tracking workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to configure VPN credentials, OpenVPN server files, rotation intervals, and command-line or Python usage patterns for workflows that need changing network egress IPs. It is intended for legitimate data collection, automated testing, price monitoring, and SEO rank tracking where VPN use is permitted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to configure persistent passwordless sudo for VPN-related commands. <br>
Mitigation: Do not add the suggested sudoers entry as written; use exact absolute paths, least-privilege wrappers, and manual administrator review. <br>
Risk: VPN credentials are stored in ~/.vpn/creds.txt and could be exposed through backups, repositories, or overly broad file access. <br>
Mitigation: Keep the credential file at owner-only permissions, exclude it from backups and repositories, and rotate VPN credentials if exposure is suspected. <br>
Risk: Agent-managed VPN rotation can disrupt local network state or route traffic through unintended egress endpoints. <br>
Mitigation: Install only when comfortable with the agent managing VPN state on the machine, and review requested connection, disconnection, and rotation commands before running them. <br>


## Reference(s): <br>
- [Vpn Rotator Free on ClawHub](https://clawhub.ai/thcjp/skills/vpn-rotator-free) <br>
- [Declared project homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, Python snippets, configuration paths, and JSON-style status output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include commands that affect local VPN state and administrative configuration; review commands before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
