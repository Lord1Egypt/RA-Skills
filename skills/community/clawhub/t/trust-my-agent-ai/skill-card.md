## Description: <br>
TrustMyAgent monitors security posture for AI agents by running stateless checks, calculating a trust score, and supporting dry-run and local-only modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Anecdotes-Yair](https://clawhub.ai/user/Anecdotes-Yair) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and security operators use this skill to assess an AI agent host, review local security check results, and decide whether to publish posture telemetry to a Trust Center dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner inspects broad local security signals and may reveal sensitive posture details. <br>
Mitigation: Run the dry-run mode first and review the exact JSON payload before allowing any results to leave the machine. <br>
Risk: Default telemetry can publish detailed posture results to an external Trust Center. <br>
Mitigation: Use local-only mode when external reporting is not desired, and only send telemetry after explicit user consent. <br>
Risk: Some enrichment or notification behavior may still involve network activity or an npx fallback in certain modes. <br>
Mitigation: Use --no-notify to avoid notification fallback behavior and review network-related options before running in sensitive environments. <br>
Risk: Recurring cron-based scans can repeatedly inspect and report agent posture. <br>
Mitigation: Enable scheduled scans only after confirming the desired interval, telemetry setting, and operational owner. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Anecdotes-Yair/trust-my-agent-ai) <br>
- [TrustMyAgent Website](https://www.trustmyagent.ai) <br>
- [Trust Center](https://www.trustmyagent.ai/trust-center.html) <br>
- [Source Repository](https://github.com/Anecdotes-Yair/trust-my-agent-ai) <br>
- [Trust Center Server Repository](https://github.com/Anecdotes-Yair/trust-my-agent-ai-website) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, configuration guidance] <br>
**Output Format:** [Markdown guidance with shell commands and structured scan or telemetry output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local assessment results, trust scores, dry-run telemetry previews, notification status, and optional scheduling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
