## Description:

Runtime Verifier helps agents verify code changes by running the app, endpoint, or CLI flow instead of relying only on unit tests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wimi321](https://clawhub.ai/user/wimi321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to plan, run, and report live runtime verification for changed applications, endpoints, or CLI flows. It is useful when observable runtime behavior matters more than unit test coverage alone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime verification may execute project code, services, or startup commands with local side effects.

Mitigation: Confirm the requested startup commands and runtime checks are appropriate for the project before running them, then clean up any started processes.

Risk: An agent could mistake unit test coverage for proof that the live runtime behavior works.

Mitigation: Exercise the changed behavior in a running app, endpoint, or CLI flow and report explicit pass/fail evidence.

## Reference(s):

- [Runtime Verifier ClawHub Skill Page](https://clawhub.ai/wimi321/skills/runtime-verifier)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with verification steps, runtime commands, pass/fail evidence, and cleanup summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No structured post-processing is required.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
