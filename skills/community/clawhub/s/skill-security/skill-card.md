## Description: <br>
Security audit tool for OpenClaw skills that scans for credential harvesting, code injection, network exfiltration, and obfuscation before installing or reviewing external skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suryast](https://clawhub.ai/user/suryast) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to audit OpenClaw skill directories before installation, review findings by severity, and manage local allowlist or blocklist decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner can produce fragile trust or block decisions because pattern matches and the pre-populated allowlist are only advisory signals. <br>
Mitigation: Manually review clean and flagged results, confirm the publisher and code behavior, and avoid relying on skill names alone for trust or provenance. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/suryast/skill-security) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Shell commands, Configuration] <br>
**Output Format:** [Terminal output with severity summaries and local allowlist or blocklist file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scanner results are advisory and require manual review before trust decisions.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
