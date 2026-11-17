## Description:

Autonomous optimization loop inspired by Andrej Karpathy's autoresearch: edit, experiment, measure, keep or revert. Best for any task with a numeric metric.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marlandoj](https://clawhub.ai/user/marlandoj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run autonomous optimization campaigns for tasks with a numeric metric, such as prompt tuning, backtest parameter optimization, site performance work, or model hyperparameter iteration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run setup, experiment, executor, and metric-extraction shell commands with broad access to the target repository.

Mitigation: Use only trusted program.md files and executor commands, and run campaigns in an isolated disposable repository or container.

Risk: The loop can edit files, create commits, and reset unsuccessful commits while optimizing against a single metric.

Mitigation: Use a dedicated branch, keep backups or remotes available, and review proposed target-file changes before accepting results into important work.

Risk: The MCP server can start background autoloop work, report results, and stop running processes.

Mitigation: Expose the MCP server only to trusted local clients, scope the results directory narrowly, and monitor running jobs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/marlandoj/skills/zouroboros-autoloop)
- [Zouroboros OpenClaw Repository](https://github.com/AlaricHQ/zouroboros-openclaw)
- [Autoloop Package Source](https://github.com/AlaricHQ/zouroboros-openclaw/tree/main/packages/autoloop)
- [Autoloop Hello Example](https://github.com/AlaricHQ/zouroboros-openclaw-examples/tree/main/examples/autoloop-hello)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Markdown, Configuration, Text]

**Output Format:** [Markdown program specifications, target-file edits, shell command execution, results.tsv records, and Markdown summary reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates git branches and commits while recording metric outcomes for each experiment.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
