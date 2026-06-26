## Description: <br>
Audits OpenClaw deployments for configuration weaknesses, exposed secrets, malicious skills, indicators of compromise, and related security risks without modifying local configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nx4dm1n](https://clawhub.ai/user/nx4dm1n) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to run local, read-only security checks against OpenClaw deployments and review prioritized findings before hardening or production use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit reports can expose local paths, configuration weaknesses, secret names, and partial credential matches. <br>
Mitigation: Treat console and JSON reports as sensitive security artifacts, store them locally, and redact details before external sharing. <br>
Risk: Running the audit with unnecessary elevated privileges can broaden the local files and environment variables it can inspect. <br>
Mitigation: Run it with the least privileges needed for the intended OpenClaw environment. <br>


## Reference(s): <br>
- [ClawHub sec-audit skill page](https://clawhub.ai/nx4dm1n/sec-audit) <br>
- [Publisher profile](https://clawhub.ai/user/nx4dm1n) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Console text or JSON security audit report with prioritized findings and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally and does not transmit audit results externally according to the release evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
