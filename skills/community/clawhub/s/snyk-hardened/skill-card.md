## Description: <br>
Comprehensive security analysis and vulnerability assessment: threat modeling, secure code review, and pre-deployment security validation across application and infrastructure layers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and application teams use this skill to run Snyk-backed security scans, prioritize vulnerabilities, and produce actionable remediation guidance before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Snyk authentication and may access sensitive vulnerability data. <br>
Mitigation: Use the normal Snyk authentication flow, verify auth status before scans, and never paste, print, or store Snyk tokens in files or conversation output. <br>
Risk: A scan could target the wrong project directory or Snyk organization. <br>
Mitigation: Confirm the absolute target path and Snyk organization before running scans, especially when switching between organizations or environments. <br>
Risk: Scan metadata or findings may be sent to Snyk and can reveal project security posture. <br>
Mitigation: Run scans only for authorized projects and organizations, and treat generated findings as confidential security information. <br>
Risk: Repeated identical scans can waste Snyk API quota without improving confidence. <br>
Mitigation: Run a single scan for a stable project state and investigate environment or dependency-lock changes when results appear inconsistent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/snyk-hardened) <br>
- [Publisher profile](https://clawhub.ai/user/snazar-faberlens) <br>
- [Faberlens safety evaluation](https://faberlens.ai/explore/snyk) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown security assessment with findings, remediation steps, and optional Snyk MCP tool calls.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference Snyk scan results, CVSS or EPSS prioritization, compliance context, and concrete remediation examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
