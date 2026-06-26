## Description: <br>
Fast OSINT and reconnaissance presets using bbot and nmap for one-command subdomain enumeration, port scanning, and web fingerprinting in bug bounty recon. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hostilespider](https://clawhub.ai/user/hostilespider) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and bug bounty researchers use this skill to run preset reconnaissance workflows for authorized targets, including subdomain enumeration, port scanning, HTTP probing, and passive recon. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reconnaissance presets may contact target systems and create logs or alerts. <br>
Mitigation: Use the skill only for domains the operator is authorized to test and confirm program scope before scanning. <br>
Risk: Scan outputs may contain sensitive target data. <br>
Mitigation: Store recon output in locations appropriate for sensitive security data and restrict access as needed. <br>
Risk: The skill depends on locally installed bbot and nmap. <br>
Mitigation: Review and trust the installation sources for bbot and nmap before running the presets locally. <br>


## Reference(s): <br>
- [Recon Quick on ClawHub](https://clawhub.ai/hostilespider/recon-quick) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and local text or JSON scan result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local recon output directories containing subdomain, port, HTTP probing, and optional JSON result files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
