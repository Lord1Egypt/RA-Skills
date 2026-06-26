## Description: <br>
Performs local network scans using Nmap to detect vulnerabilities, identify service versions, and fingerprint operating systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JacquesLauren](https://clawhub.ai/user/JacquesLauren) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security engineers use this skill to run authorized Nmap-based assessments against specified hosts or network ranges and review structured scan results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Network scanning can affect systems outside the intended scope or violate policy when used without authorization. <br>
Mitigation: Confirm the exact host or CIDR range before scanning and only scan systems you own or have explicit permission to test. <br>
Risk: The skill runs the local Nmap binary, so results and behavior depend on the installed tool. <br>
Mitigation: Use a trusted Nmap installation that is available in PATH before running assessments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JacquesLauren/tech-security-audit) <br>
- [Publisher profile](https://clawhub.ai/user/JacquesLauren) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and Python callable output as structured dictionaries parsed from Nmap XML] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Nmap installed and accessible in PATH; scan behavior depends on the selected target and scan type.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
