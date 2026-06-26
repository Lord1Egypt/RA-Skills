## Description: <br>
Guides SecOps endpoint checks for EDR, Sysmon, updates, EVTX heartbeat alerts, least privilege, network visibility, credential protection, vulnerability inventory, weekly assessment, and skill integrity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inaor](https://clawhub.ai/user/inaor) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
SecOps engineers, endpoint administrators, and developers use this skill to review Windows host posture, design heartbeat and alert logic, and produce concise security assessment reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Endpoint security checks can expose sensitive host, log, network, credential-hardening, and vulnerability details. <br>
Mitigation: Limit use to authorized endpoints and data sources, summarize results as counts and statuses where possible, and avoid collecting raw logs, PII, full network tables, or full vulnerability payloads unless explicitly needed. <br>
Risk: Skill integrity baselines and assessment outputs could disclose operational state if broadly reported. <br>
Mitigation: Keep hash baselines local unless reporting is deliberately configured, send only metadata such as hashes and changed file names, and define approved reporting destinations before enabling recurring checks. <br>
Risk: Generated security commands or posture recommendations may be incorrect for a specific Windows environment or policy. <br>
Mitigation: Review commands and recommendations before execution, scope EVTX queries to relevant time windows, and validate policy thresholds such as patch age, EDR health, and privilege expectations with the operating team. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/inaor/secops-by-joes) <br>
- [Security Joes](https://www.securityjoes.com) <br>
- [Security Joes About](https://www.securityjoes.com/about) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline PowerShell commands and structured status fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include host posture fields, event summaries, hashes, and vulnerability counts; avoid raw logs and PII when following the skill guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
