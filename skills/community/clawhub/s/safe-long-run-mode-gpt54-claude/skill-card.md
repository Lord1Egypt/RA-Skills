## Description:

Operate long-running AI tasks safely across GPT-5.4 and Claude by using model selection rules, phased execution, checkpoints, resumable workflows, API throttling discipline, and subagent isolation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bwiley1989](https://clawhub.ai/user/bwiley1989)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to keep long-running agent work organized and resumable across coding, documentation, research, browser automation, cloud, and external API tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may add process overhead for short tasks.

Mitigation: Use it for longer or riskier work where phased execution, checkpoints, and handoff notes are worth the extra structure.

Risk: The skill encourages local checkpoint artifacts that may contain task details.

Mitigation: Review checkpoint locations and contents before using it with sensitive projects or shared workspaces.

Risk: The model-routing preferences may not match every organization, task, or trust boundary.

Mitigation: Confirm whether the GPT-5.4 and Claude routing guidance fits the task before applying it.

Risk: Long-running cloud, browser, GUI, or external API tasks can throttle or fail mid-run.

Mitigation: Use the skill's batching, retry, checkpoint, and stop-condition guidance before starting those workflows.

## Reference(s):

- [Safe Long-Run Checklist](references/checklist.md)
- [ClawHub skill page](https://clawhub.ai/bwiley1989/skills/safe-long-run-mode-gpt54-claude)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown prose, checklists, and inline commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include checkpoint files, phase summaries, resume notes, and model-routing recommendations.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
