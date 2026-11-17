## Description:

Super Agent Loop orchestrates dependency-aware agent workflows by executing DAG steps, self-verifying node outputs, storing reusable memory, and reflecting on failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to run long-horizon workflows where dependent steps must execute in order, pass verification gates, reuse prior results, and produce failure diagnostics when downstream work is blocked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Loop JSON files can cause shell commands to run during workflow execution.

Mitigation: Treat loop definitions as executable input: use trusted files only, review every run command before execution, and run in a sandbox or low-privilege workspace.

Risk: The learner helper can write learning state into a caller-supplied skill directory.

Mitigation: Pass only the intended skill directory to learner commands and avoid sensitive or shared directories for learning state.

Risk: Dependency cycles are not reported and can leave graph nodes permanently blocked.

Mitigation: Validate workflow graphs as DAGs before running and review blocked-node reports before reusing their results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/super-agent-loop)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [JSON execution reports, memory files, and human-readable guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses caller-provided graph definitions, action functions, verification functions, and output directories.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
