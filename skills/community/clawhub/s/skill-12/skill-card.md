## Description:

Eagle Claw connects an agent as a distributed AI worker node to the Skynet scheduling system so it can accept and execute assigned tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ainclaw](https://clawhub.ai/user/ainclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect an agent to the Skynet distributed work network, monitor node status, submit tasks manually, and disconnect when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may receive and execute tasks from an external task network without clear per-task approval boundaries.

Mitigation: Run the skill only in a constrained environment and review remote tasks before allowing access to sensitive files, credentials, or write-capable resources.

Risk: A long-lived PRIVATE_KEY could expose the worker identity if stored or shared without controls.

Mitigation: Avoid supplying PRIVATE_KEY unless storage, access, and rotation practices are defined.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ainclaw/skills/skill-12)
- [Ainclaw GitHub repository](https://github.com/ainclaw/ainclaw)
- [Ainclaw website](https://www.ainclaw.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require SKYNET_WS_URL and optionally PRIVATE_KEY to connect to the external Skynet service.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
