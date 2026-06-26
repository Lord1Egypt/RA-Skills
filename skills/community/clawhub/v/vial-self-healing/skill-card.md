## Description: <br>
Vial self-healing runtime — 8 protocols covering technical failures, behavioral failures, and agent role enforcement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adrianhihi](https://clawhub.ai/user/adrianhihi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to guide recovery from common agent failures such as authorization errors, rate limits, timeouts, silent failures, loop behavior, and role drift. It also provides logging and telemetry patterns for improving repair strategies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A remote repair service and broad automatic recovery rules can influence agent behavior. <br>
Mitigation: Install only if the publisher is trusted, and keep explicit confirmation plus read-only verification boundaries around sensitive workflows. <br>
Risk: The skill sends anonymous telemetry and writes local log entries under /tmp. <br>
Mitigation: Review the disclosed telemetry fields before deployment and avoid environments where outbound telemetry or local temporary logging is not acceptable. <br>
Risk: Security evidence advises avoiding sensitive, financial, purchase, account-changing, or public-posting workflows without controls. <br>
Mitigation: Require user confirmation for irreversible actions and verify outcomes with read-only checks before reporting completion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adrianhihi/vial-self-healing) <br>
- [Skill homepage](https://github.com/adrianhihi/helix) <br>
- [Telemetry endpoint disclosed in metadata](https://helix-telemetry.haimobai-adrian.workers.dev/v1/event) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May query remote repair guidance, send anonymous telemetry fields, and write local /tmp/vial.log entries.] <br>

## Skill Version(s): <br>
0.6.3 (source: server release evidence and openclaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
