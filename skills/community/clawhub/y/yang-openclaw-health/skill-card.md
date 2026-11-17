## Description:

Quick health check for OpenClaw installations that checks Node.js version, gateway status, config files, port conflicts, and common configuration problems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to run local diagnostics when troubleshooting OpenClaw installation or configuration issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The diagnostic script inspects local OpenClaw files, process or port state, and whether common model API-key environment variables are present.

Mitigation: Run it only from a trusted ClawHub source and review console output before sharing diagnostics; the provided security evidence says inspected code does not print key values or send them anywhere.

Risk: The script runs local process and port checks that may behave differently when required platform utilities are unavailable.

Mitigation: Treat skipped or inconclusive checks as prompts for manual verification of gateway status, port 3000 usage, and OpenClaw configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/skills/yang-openclaw-health)
- [OpenClaw installation service](https://yang1002378395-cmyk.github.io/openclaw-install-service/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Console text with diagnostic status lines and suggested shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Manual local diagnostic script output; no network transmission is described in the provided security evidence.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
