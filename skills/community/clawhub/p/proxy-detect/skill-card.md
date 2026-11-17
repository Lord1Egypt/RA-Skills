## Description:

Detects active system proxy settings on Windows and macOS, tests proxy availability, and returns results in JSON format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noah-smith-max](https://clawhub.ai/user/noah-smith-max)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to check whether an environment has an active system or common local proxy and to receive the detected proxy address in JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proxy configuration may be exposed in console output or logs.

Mitigation: Run the skill only where proxy address disclosure is acceptable, and avoid sharing logs that include detected proxy details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/noah-smith-max/skills/proxy-detect)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Console text with a JSON object containing address and isActive fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.6+ and no external dependencies.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
