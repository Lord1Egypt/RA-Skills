## Description:

Orchestrate small development workflows: parse requirements, spawn two persistent subagents (coding and testing, each with isolated 128k context), loop until tests pass, and produce local git commits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yufengwolf](https://clawhub.ai/user/yufengwolf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to coordinate small implementation-and-test workflows with separate coding and testing workers, iterative retry behavior, local result artifacts, and local git commits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write result files, maintain persistent workflow state, create local commits, and execute generated test artifacts.

Mitigation: Use it only in repositories where those actions are acceptable, inspect generated changes before relying on them, and prefer a disposable sandbox or container with limited filesystem and credential access.

Risk: Untrusted archives or workflow IDs could affect local workflow execution.

Mitigation: Do not provide untrusted archives or workflow IDs, and review workflow inputs before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yufengwolf/skills/workflow-runner)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, code changes, JSON result artifacts, and local git commits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local results under results/ and may keep persistent workflow state for worker sessions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
