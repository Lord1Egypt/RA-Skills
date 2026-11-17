## Description:

Execute the next workable node of the TODO.md task tree end to end, driven by each task's status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bassemzohdy](https://clawhub.ai/user/bassemzohdy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to select and complete a workable TODO.md task, following its status through branching, implementation, verification, and completion. Optional flags support planning, lane runs, worktrees, delegation, and merging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security analysis was partial because referenced files were absent from the scanned artifact, leaving medium confidence.

Mitigation: Review the referenced files and the skill's behavior before installing or running it.

## Reference(s):

- [Source skill (server-resolved GitHub provenance)](https://github.com/bassemZohdy/todo-skills/tree/main/plugin/skills/todo-continue)
- [ClawHub skill release](https://clawhub.ai/bassemzohdy/skills/todo-continue)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Markdown, Guidance]

**Output Format:** [Code and repository changes with Markdown guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Completes at most one task node per invocation, except lane runs.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
