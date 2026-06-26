## Description: <br>
Security vitals checker for OpenClaw. Scans your installation, scores your setup, and shows you exactly what to fix. First scan in seconds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bk-cm](https://clawhub.ai/user/bk-cm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw administrators and developers use SecurityVitals to run point-in-time security health checks on self-hosted OpenClaw installations and receive scored remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides an agent to execute local OpenClaw and Node.js commands. <br>
Mitigation: Review the five documented commands before approving execution and skip update status when a fully offline scan is required. <br>
Risk: Local command output may contain sensitive operational details. <br>
Mitigation: Extract only the documented fields and do not display API keys, tokens, credentials, secrets, or raw command output. <br>
Risk: Point-in-time checks can become stale and may not represent ongoing security posture. <br>
Mitigation: Treat each report as a current snapshot and rerun the scan after configuration, version, or deployment changes. <br>


## Reference(s): <br>
- [SecurityVitals ClawHub Listing](https://clawhub.ai/bk-cm/securityvitals) <br>
- [ClawVitals Website](https://clawvitals.io) <br>
- [ClawVitals Documentation](https://clawvitals.io/docs) <br>
- [ClawVitals Controls](https://clawvitals.io/docs/controls) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with a scored control table, optional detail report, and remediation text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stateless point-in-time report; stable controls are scored and experimental notes are reported separately.] <br>

## Skill Version(s): <br>
1.4.8 (source: server release and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
