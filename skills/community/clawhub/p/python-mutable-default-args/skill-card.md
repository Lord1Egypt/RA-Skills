## Description:

A Python function uses a mutable object (list, dict, set) as a default argument, sharing state across calls in a way that produces silent bugs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mvogt99](https://clawhub.ai/user/mvogt99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill during Python code review to identify mutable default argument bugs and apply the canonical None-default initialization pattern.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may flag deliberate stateful defaults, such as a documented cache, as defects.

Mitigation: Review the function's intent before changing behavior and keep intentional stateful defaults only when they are clearly documented.

Risk: Refactoring a mutable default can change behavior for callers that accidentally relied on shared state across calls.

Mitigation: Add or update tests around repeated calls before applying the None-default initialization pattern.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mvogt99/skills/python-mutable-default-args)

## Skill Output:

**Output Type(s):** [Guidance, Code]

**Output Format:** [Markdown with Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No tool execution or external service calls are required.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
