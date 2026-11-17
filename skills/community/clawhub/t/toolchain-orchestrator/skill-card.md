## Description:

Toolchain Orchestrator helps an agent define multi-tool workflows as dependency DAGs, validate them, execute them in topological order, pass upstream output through {{node_id}} placeholders, rerun from failed steps, and export workflow visualizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to plan, validate, run, resume, and visualize multi-step command workflows where each step may depend on earlier tool output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill executes shell commands from chain files.

Mitigation: Review chain files before execution, run only trusted workflows, use a sandbox or least-privileged account, and validate or dry-run before running commands.

Risk: Prior command output can be inserted into later commands through {{node_id}} placeholders.

Mitigation: Avoid passing untrusted command output into placeholders, and quote or sanitize values before they become part of later shell commands.

Risk: The learner records operation history, errors, notes, preferences, and improvement suggestions.

Mitigation: Disable or remove the learner when persistent local history is not desired, and inspect stored learning files before sharing the skill package.

## Reference(s):

- [Skill documentation](artifact/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/toolchain-orchestrator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON or YAML chain definitions, bash command examples, and generated workflow artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce validation results, dry-run plans, run logs, captured stdout files, and DOT graph output when the orchestrator commands are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
