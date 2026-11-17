## Description:

Explore capability boundaries of a target Skill, analyze optimization potential, generate an optimized version using Training-Free GRPO, and compile results into a structured report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[t1ans1r](https://clawhub.ai/user/t1ans1r)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to evaluate another agent skill, generate training and test tasks, create an optimized copy, execute comparisons, analyze failures, and produce a results report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute commands and install dependencies based on target-skill behavior.

Mitigation: Run it only in a disposable container or VM, pass a narrow target skill directory, disable auto_install_deps, and review commands before execution.

Risk: The skill relies on API credentials for LLM-powered optimization and evaluation.

Mitigation: Avoid exposing unrelated secrets in the environment and provide only the credentials required for the intended run.

Risk: Generated optimization suggestions or modified skill copies can introduce incorrect or misleading behavior.

Mitigation: Review generated changes, scan the optimized skill before deployment, and compare the results report against the original skill.

## Reference(s):

- [ClawHub Skills Coach release page](https://clawhub.ai/t1ans1r/skills/skills-coach)
- [Skills-Coach README](artifact/README.md)
- [Training-Free GRPO notes](artifact/archive/docs/README_TRAINING_FREE_GRPO.md)
- [Training-Free GRPO implementation reference](https://github.com/TencentCloudADP/youtu-agent/tree/training_free_GRPO)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, JSON metadata, generated task files, optimized skill files, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create timestamped run directories, optimized skill copies, execution logs, failure analyses, and results reports.]

## Skill Version(s):

2.3.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
