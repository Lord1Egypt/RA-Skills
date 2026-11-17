## Description:

Shared mutable state is accessed from concurrent contexts without synchronization, producing nondeterministic behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mvogt99](https://clawhub.ai/user/mvogt99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to recognize race conditions in concurrent code and choose safer synchronization, atomicity, immutability, message-passing, and testing approaches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Concurrency guidance may be applied to the wrong shared state boundary or synchronization primitive.

Mitigation: Review the affected code path, identify all readers and writers, and validate the chosen fix with concurrency-focused tests.

Risk: A suggested lock or atomic operation could reduce throughput or leave a check-then-act sequence partially protected.

Mitigation: Keep critical sections narrow, document protected state, and prefer database or platform-provided atomic operations where applicable.

## Reference(s):

- [Race Condition on ClawHub](https://clawhub.ai/mvogt99/skills/race-condition)

## Skill Output:

**Output Type(s):** [guidance, code]

**Output Format:** [Markdown guidance with optional inline code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executable reference guidance]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
