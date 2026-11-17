## Description:

Analyze Python type annotation coverage and quality by checking mypy compliance, finding untyped functions, reviewing Protocol and Generic usage, TypeVar constraints, and modern typing patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit Python type safety, prepare projects for stricter mypy settings, and prioritize fixes for weak or missing type annotations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects local Python source files and may surface file paths or code snippets in its analysis.

Mitigation: Run it only in the intended workspace and review generated findings before sharing them outside the project.

Risk: Broad shell searches or optional type-checker runs can produce noisy results when run from the wrong directory or across vendored dependencies.

Mitigation: Run commands from the project root and exclude virtual environments, build outputs, and third-party code where appropriate.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with inline shell commands and code recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file paths, command output summaries, coverage counts, and recommended mypy settings.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
