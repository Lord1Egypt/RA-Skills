## Description:

Autonomous space navigation agent using optical quantum kernels for terrain classification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aadipapp](https://clawhub.ai/user/aadipapp)

### License/Terms of Use:

MIT

## Use Case:

External developers and engineers can use this skill to run a local simulation that classifies space-terrain sensor readings and returns proceed, avoid, halt, or safe-mode decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Malformed sensor input can bypass the advertised safety check and return a PROCEED decision.

Mitigation: Validate sensor input shape and values before execution, and fail closed to safe mode on malformed or out-of-range input.

Risk: The skill presents navigation-style decisions that may be mistaken for safety-critical autonomy behavior.

Mitigation: Use it only as a local simulation unless the decision logic, input validation, and fail-closed behavior are independently reviewed for the deployment context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aadipapp/skills/space-autonomy-skill)
- [Publisher profile](https://clawhub.ai/user/aadipapp)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local simulation output includes terrain kernel scores, the best terrain match, confidence, and a navigation decision.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
