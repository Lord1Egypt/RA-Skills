## Description:

Comprehensive Elixir/Phoenix code review with optional parallel agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering reviewers use this skill to review Elixir and Phoenix code changes, run normal Mix project checks, load applicable companion review skills, and produce a structured review with issues, fixes, good patterns, and a verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides an agent to run normal Elixir project review commands in the target repository.

Mitigation: Use it only on codebases where running Mix tasks and optional tests is acceptable.

Risk: The full review workflow can depend on referenced companion review skills.

Mitigation: Confirm the companion review skills are available when the full Elixir, Phoenix, LiveView, performance, security, or ExUnit workflow is needed.

## Reference(s):

- [Review Elixir skill page](https://clawhub.ai/anderskev/skills/review-elixir)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Structured Markdown review with issue severity sections, FILE:LINE references, recommended fixes, good patterns, and a verdict.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run Mix formatter, Credo, Dialyzer, and tests where present; the --parallel flag can use specialized subagents when the host agent supports them.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
