## Description: <br>
Security Monitor V15 T33 helps agents audit Linux/Unix servers for suspicious processes, risky network exposure, file-permission issues, sensitive information in local files, anomalous logs, and process-tree concerns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[t33-coder](https://clawhub.ai/user/t33-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and system administrators use this skill to inspect servers they administer, triage suspicious activity, and produce security audit findings that can guide follow-up remediation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security scan reports may expose host details, running processes, network endpoints, file paths, and potential secrets. <br>
Mitigation: Restrict permissions on saved reports and logs, and redact sensitive findings before sharing them. <br>
Risk: Running broad scans with elevated privileges can collect more sensitive system information than needed. <br>
Mitigation: Use sudo only when required for the intended audit and prefer targeted directories or checks when a full-system scan is unnecessary. <br>
Risk: Findings from heuristic process, port, log, and secret checks can include false positives. <br>
Mitigation: Have an administrator validate findings before terminating processes, changing firewall rules, rotating credentials, or escalating an incident. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/t33-coder/security-monitor-v15-t33) <br>
- [Server Security Checklist](references/security-checklist.md) <br>
- [Common Service Port Reference](references/common-ports.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell and Python code blocks; the monitor script can also emit human-readable text and JSON-formatted results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Audit reports can contain sensitive host, process, network, path, and secret-finding details and should be stored and shared with restricted access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
