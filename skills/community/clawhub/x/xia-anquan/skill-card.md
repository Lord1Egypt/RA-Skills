## Description: <br>
虾安全 is an OpenClaw security monitoring skill that checks Capability, Identity, and Knowledge state for persistent state pollution, credential exfiltration, suspicious URLs, dynamic code execution, and dangerous deletion patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luis1213899](https://clawhub.ai/user/luis1213899) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to audit an OpenClaw workspace for CIK security issues across identity files, memory state, and installed skill scripts. It can run a one-time audit, emit JSON for other tools, or run periodic monitoring with local alert logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local audit snapshots and alert logs can contain sensitive workspace or security findings. <br>
Mitigation: Restrict access to ~/.cik-audit and periodically review or delete retained snapshots and logs, especially on shared or broadly backed-up systems. <br>
Risk: The monitor mode runs repeated local audits and persists state and logs over time. <br>
Mitigation: Run daemon mode only where ongoing local monitoring is intended, and choose an interval that matches operational needs. <br>


## Reference(s): <br>
- [Your Agent, Their Asset: A Real-World Safety Analysis of OpenClaw](https://arxiv.org/abs/2604.04759) <br>
- [ClawHub skill page](https://clawhub.ai/luis1213899/xia-anquan) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Console text, optional JSON, and local audit snapshot and alert log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs with Node.js 18+ and writes audit history under ~/.cik-audit when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, _meta.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
