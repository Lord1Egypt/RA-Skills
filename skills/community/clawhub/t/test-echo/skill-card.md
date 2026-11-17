## Description:

A test echo skill for testing OpenClaw skill system with parameter passing.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[pplx1104](https://clawhub.ai/user/pplx1104)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and testers use Test Echo to verify OpenClaw skill parameter passing by returning a greeting for a provided name.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reflects the provided name in its output, so sensitive values entered as the name could be returned to the caller.

Mitigation: Use non-sensitive test names and avoid entering secrets or confidential data as the name parameter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pplx1104/skills/test-echo)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [JSON string containing status, message, and echoed input fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reflects the provided name in the response; no file, network, credential, persistence, or privilege behavior was identified in the authoritative security evidence.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
