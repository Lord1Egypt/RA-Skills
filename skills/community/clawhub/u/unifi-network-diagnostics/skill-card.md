## Description:

Diagnoses private household UniFi network issues and discovers non-secret local helper configuration for read-only troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catholicbeer](https://clawhub.ai/user/catholicbeer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and network operators use this skill to diagnose household UniFi Wi-Fi, DNS, WAN, latency, packet loss, device health, and suspicious-device symptoms. It guides agents toward bounded read-only tests and requires explicit owner approval before state-changing remediation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute a locally discovered UniFi helper.

Mitigation: Verify the exact helper path and trustworthiness before approving configuration writes or helper use.

Risk: Network diagnostic output can contain private identifiers or topology details.

Mitigation: Review diagnostic output before sharing it and redact private network names, paths, MAC addresses, topology details, and public WAN information.

Risk: State-changing network actions could interrupt connectivity or alter UniFi configuration.

Mitigation: Require explicit owner approval and a stated action, expected effect, risk, and stop or rollback condition before any remediation.

## Reference(s):

- [Diagnostic Model](references/diagnostic-model.md)
- [ClawHub skill page](https://clawhub.ai/catholicbeer/skills/unifi-network-diagnostics)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown diagnostic report with observations, inferences, ranked hypotheses, confidence, unresolved questions, and recommended next action]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bounded read-only shell diagnostics and redacted JSON evidence from local scripts.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
