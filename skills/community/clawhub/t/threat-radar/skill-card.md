## Description: <br>
Threat Radar helps agents run local security posture checks across Docker images, dependencies, service ports, SSL/TLS targets, and OpenClaw configuration, with CVE-oriented status and report output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariusfit](https://clawhub.ai/user/mariusfit) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators of OpenClaw or homelab infrastructure use this skill to run local security scans, review CVE-oriented findings, and generate status or report output before deciding on remediation. Treat its findings as advisory because the server security review says the release overstates its CVE, alerting, and scheduling capabilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release may overstate CVE feed retrieval, alerting, and scheduling behavior, which can create false confidence in the scan results. <br>
Mitigation: Use it as a lightweight local prototype, verify vulnerability results with independent tools or authoritative feeds, and confirm alerting and scheduling behavior before relying on it. <br>
Risk: Local scans can inspect package files, Docker image listings, service ports, SSL targets, and OpenClaw configuration while producing reports and logs. <br>
Mitigation: Review the configuration before scanning, run it only in the intended workspace, and keep generated reports, databases, and logs private. <br>
Risk: Host command coverage depends on installed tools and permissions for commands such as Docker and OpenSSL. <br>
Mitigation: Check tool availability and permissions up front, and treat missing or empty scan sections as inconclusive rather than clean results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mariusfit/threat-radar) <br>
- [Publisher profile](https://clawhub.ai/user/mariusfit) <br>
- [NVD CVE detail example](https://nvd.nist.gov/vuln/detail/CVE-2021-23337) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text, JSON status output, and Markdown-style reports with inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local configuration, scan history, CVE cache, and log files under the OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact header) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
