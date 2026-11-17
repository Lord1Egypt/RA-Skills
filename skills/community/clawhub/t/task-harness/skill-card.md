## Description:

Task Harness helps agents break larger development requests into structured task lists and create a persistent workflow harness for long-running, multi-session work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kangarooking](https://clawhub.ai/user/kangarooking)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to plan multi-session implementation work, track feature completion, restore context between sessions, and produce the task, progress, and initialization files that guide future agent runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to add persistent workflow rules to AGENTS.md, which can affect future agent behavior across sessions.

Mitigation: Review the exact AGENTS.md diff before accepting persistent workflow rules.

Risk: The skill's workflow includes git commit and push steps after feature completion.

Mitigation: Require explicit review of the changed files, destination remote, and branch before allowing commits or pushes.

## Reference(s):

- [Task Harness Methodology](references/methodology.md)
- [Feature List Template](references/templates/feature_list.json)
- [Progress Log Template](references/templates/progress.txt)
- [Initialization Script Template](references/templates/init.sh)
- [Task Overview Template](references/templates/task.json)
- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON templates and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces repository-resident harness files such as feature_list.json, progress.txt, init.sh, task.json, and AGENTS.md workflow guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
