## Description:

Tasktodolist manages multiple independent local to-do lists with commands to add, list, complete, remove, clear, and delete named lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guiguihao](https://clawhub.ai/user/guiguihao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to maintain simple local task lists from a terminal, with separate lists selected by task name.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task names containing path separators or '..' may let file operations escape the documented ~/.tasktodolist data folder.

Mitigation: Review before installing, avoid untrusted or unusual task names, and require task-name validation that confines reads, writes, and deletes to ~/.tasktodolist.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guiguihao/skills/tasktodolist)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Terminal text output from CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local todo data under ~/.tasktodolist using named JSON files.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
