## Description:

Prevent premature completion claims, repeated same-pattern retries, and weak handoffs. Use this skill to improve verification, strategy switching, and blocked-task reporting without changing personality or tone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aviclaw](https://clawhub.ai/user/aviclaw)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to check meaningful evidence before claiming work is complete, switch strategy after repeated low-signal attempts, and provide concise handoffs when blocked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may spend excessive effort verifying low-stakes tasks.

Mitigation: Apply the skill's effort calibration guidance and use the lightest meaningful check that gives real evidence.

Risk: Agents may be unable to fully verify a task when required runtime, credentials, or context are unavailable.

Mitigation: Use the blocked-task handoff pattern to state what changed, what was checked, what could not be checked, and the remaining uncertainty.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with optional commands or code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No hidden execution, persistence, credential use, or unrelated data access was identified in the server security summary.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
