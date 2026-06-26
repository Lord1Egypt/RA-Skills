## Description: <br>
Autonomous optimization loop inspired by Andrej Karpathy's autoresearch: edit, experiment, measure, keep or revert. Best for any task with a numeric metric. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marlandoj](https://clawhub.ai/user/marlandoj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to automate iterative single-metric optimization in a git repository, including prompt tuning, trading backtests, site performance work, and model hyperparameter experiments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local shell commands, edit and commit code, reset changes, and start background jobs. <br>
Mitigation: Use it in a disposable clone or container, review the program.md setup, run, metric, and executor commands before execution, and avoid repositories containing secrets or production data. <br>
Risk: Target-file contents may be sent to the configured executor. <br>
Mitigation: Use only trusted executors and keep sensitive data out of files selected for optimization. <br>
Risk: MCP tools can start, list, and stop autoloop jobs from the configured results directory. <br>
Mitigation: Limit MCP use to trusted local workspaces and supervise started loops so process ownership and command scope are clear. <br>


## Reference(s): <br>
- [Zouroboros Autoloop on ClawHub](https://clawhub.ai/marlandoj/zouroboros-autoloop) <br>
- [Zouroboros OpenClaw Repository](https://github.com/AlaricHQ/zouroboros-openclaw) <br>
- [Autoloop Hello Example](https://github.com/AlaricHQ/zouroboros-openclaw-examples/tree/main/examples/autoloop-hello) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Markdown, Configuration, Files] <br>
**Output Format:** [Markdown instructions, shell commands, git commits, TSV results, and summary reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs against a program.md specification and records experiment results in the target project.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
