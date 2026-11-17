## Description:

Test PydanticAI agents using TestModel, FunctionModel, VCR cassettes, and inline snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to write and maintain tests for PydanticAI agents, including deterministic model tests, custom model behavior, recorded API interactions, inline snapshots, tool calls, dependency overrides, and message capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: VCR recording and inline snapshot fixing can make real API calls or rewrite test files.

Mitigation: Run these commands only on scoped test paths after a baseline test run, then review the resulting diff before keeping cassette or snapshot changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anderskev/skills/pydantic-ai-testing)
- [Publisher profile](https://clawhub.ai/user/anderskev)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with Python, TOML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
