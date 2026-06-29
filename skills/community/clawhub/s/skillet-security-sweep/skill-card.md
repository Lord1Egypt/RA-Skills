## Description: <br>
Use when asked to security-audit a repository, find vulnerabilities to fix, check for leaked secrets, review dependencies for known CVEs, or harden a project before exposure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[escoffier-labs](https://clawhub.ai/user/escoffier-labs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to perform defensive repository security reviews, covering secrets, dependency vulnerabilities, input handling, authorization, and accidental exposure before a project is shared or deployed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security review output can expose sensitive findings if secret values are copied into the report. <br>
Mitigation: Report only the secret type and file location, and rotate any exposed credential before treating the issue as resolved. <br>
Risk: Security findings may be incomplete when runtime configuration or deployment context is unavailable. <br>
Mitigation: Mark configuration-dependent findings as unverified, lower their severity, and list skipped areas in the report. <br>
Risk: Operational use in a maintainer context may affect projects that contain sensitive code, packages, or production data. <br>
Mitigation: Keep reviews defensive and read-only, preserve audit trails, and review remediation commands before applying them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/escoffier-labs/skillet-security-sweep) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Analysis, Shell commands, Guidance] <br>
**Output Format:** [Markdown security audit report with findings, scorecard, remediation steps, and backlog items] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports secret locations by file, line, and type only; secret values are not copied or echoed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
