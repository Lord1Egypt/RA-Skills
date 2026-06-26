## Description: <br>
Security Guardian helps agents audit OpenClaw projects for hardcoded secrets and high-severity container vulnerabilities, then report remediation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1999AZZAR](https://clawhub.ai/user/1999AZZAR) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering agents use this skill to scan project directories for likely committed credentials and to run Trivy checks against container images before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Secret scanning recursively reads selected project files and may inspect sensitive source content. <br>
Mitigation: Limit scans to intended repositories, keep common dependency and cache exclusions enabled, and avoid --force on system paths unless explicitly required. <br>
Risk: Container scanning depends on a local Trivy installation and reports high-severity findings that require human review. <br>
Mitigation: Install Trivy from a trusted source, review reported HIGH and CRITICAL vulnerabilities, and update base images or packages before deployment. <br>
Risk: Follow-up remediation may involve vaulting credentials or changing application configuration. <br>
Mitigation: Review any vaulting, environment-variable, or code changes before applying them. <br>


## Reference(s): <br>
- [Security Guardian on ClawHub](https://clawhub.ai/1999AZZAR/security-guardian) <br>
- [Trivy documentation](https://aquasecurity.github.io/trivy/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text and Markdown-style guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Secret scans return finding type, file path, and line number; container scans report HIGH and CRITICAL vulnerability findings from Trivy.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
