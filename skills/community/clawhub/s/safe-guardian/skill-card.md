## Description:

Safe Guardian provides a JavaScript helper for checking OpenClaw-style operations against configurable blacklist and whitelist rules and recording audit logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[confidentkai](https://clawhub.ai/user/confidentkai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to screen proposed OpenClaw operations, tune blacklist and whitelist rules, and review audit logs before allowing automation workflows. It should be treated as advisory screening rather than the sole enforcement boundary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill presents itself as a protective OpenClaw enforcement layer, but server security evidence says the shipped code is a weak helper and can approve dangerous operations if users rely on the documented API.

Mitigation: Do not rely on it as an OpenClaw enforcement boundary; review proposed operations before execution and pair it with real tool interception or sandbox controls.

Risk: The documented API and implementation behavior may not match the actual tool-call shape expected by an OpenClaw integration.

Mitigation: Validate the integration API shape with tests before deployment and apply deny rules before any allow exceptions.

Risk: Initialization and default policy behavior can affect local policy files, including broad sensitive-file defaults and overwriting administrator policy.

Mitigation: Review and lock down policy files before use, remove broad sensitive-file defaults, and prevent initialization from replacing administrator-managed policy.

## Reference(s):

- [Safe Guardian ClawHub Page](https://clawhub.ai/confidentkai/skills/safe-guardian)

## Skill Output:

**Output Type(s):** [guidance, configuration, code]

**Output Format:** [JSON-like JavaScript objects, audit log entries, and concise text reasons]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns allow or block decisions with reasons; may write audit logs and policy configuration files.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter and package.json report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
