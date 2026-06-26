## Description: <br>
AgentGuard scans AI agent skills and runtime actions for security risks, audits local credentials and exposure, supports Web3 safety checks, and can generate health reports or scheduled patrol reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xbeekeeper](https://clawhub.ai/user/0xbeekeeper) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use AgentGuard to review skills, commands, network activity, credentials, Web3 actions, and OpenClaw environments before or during agent use. It is intended for security scanning, action allow/deny guidance, trust registry management, audit reporting, and local health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad local visibility into agent state, installed skills, workspaces, credential-directory metadata, environment names, network or cron status, and Web3 action context. <br>
Mitigation: Install only when this level of local security auditing is intended, and review generated reports before sharing them. <br>
Risk: Optional Web3 simulation and external package behavior may depend on configured GoPlus credentials and the installed AgentGuard package version. <br>
Mitigation: Verify the external AgentGuard package and version, and provide GoPlus API credentials only when enhanced Web3 simulation is needed. <br>
Risk: Auto-scan and daily patrol features can create ongoing local monitoring. <br>
Mitigation: Enable auto-scan or daily patrols only when continuous local monitoring is desired, and periodically review the resulting audit output. <br>


## Reference(s): <br>
- [ClawHub AgentGuard release page](https://clawhub.ai/0xbeekeeper/security) <br>
- [README](README.md) <br>
- [Scan rules reference](scan-rules.md) <br>
- [Action policies reference](action-policies.md) <br>
- [Web3 vulnerability patterns reference](web3-patterns.md) <br>
- [Patrol checks reference](patrol-checks.md) <br>
- [Evaluation scenarios](evals.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance, HTML report] <br>
**Output Format:** [Markdown reports, JSON decisions, shell command suggestions, configuration records, and generated HTML health reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local audit, trust, and configuration records under AgentGuard-managed paths when commands are run.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release evidence; skill metadata lists 1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
