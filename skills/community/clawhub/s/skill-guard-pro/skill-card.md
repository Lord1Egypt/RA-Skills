## Description: <br>
Security scanner for ClawHub skills. Analyze before you install. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChloePark85](https://clawhub.ai/user/ChloePark85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to statically inspect ClawHub skill directories or named skills before installation, with advisory labels for network endpoints, credential patterns, destructive commands, and related risky code patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Static scan labels can miss runtime behavior or overstate benign patterns. <br>
Mitigation: Treat SAFE, CAUTION, and DANGEROUS labels as advisory and manually review flagged code before relying on the result. <br>
Risk: Flagged network endpoints, credential access, or destructive commands may require context-specific judgment. <br>
Mitigation: Review any reported endpoints, credential patterns, and file deletion commands before installing or running the scanned skill. <br>


## Reference(s): <br>
- [Skill Guard Pro on ClawHub](https://clawhub.ai/ChloePark85/skill-guard-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain-text or JSON security report with SAFE, CAUTION, or DANGEROUS risk labels] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes advisory scan findings, discovered URLs, risk score, files scanned, lines scanned, and exit codes suitable for scripts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
