## Description:

Use when a user needs to add a new task or record a pending to-do item; when prompting an Agent to execute a pending task; during Agent heartbeat events to pick up and work on tasks; when a user expresses interest in a topic for later research, saves a bookmark for processing, or asks for help preparing deliverables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liusining](https://clawhub.ai/user/liusining)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to maintain a shared Markdown task board, add tasks with expected outcomes, let agents pick up pending work, and record progress for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Editable task names and notes can drive agent work, including unattended heartbeat processing.

Mitigation: Use trusted task boards, review requirements before execution, and disable automatic heartbeat pickup unless unattended task processing is intended.

Risk: Task names containing path characters can cause Markdown notes to be written outside the intended notes folder.

Mitigation: Choose a confined notes folder and avoid task names containing path separators or traversal characters.

Risk: The skill depends on PyYAML for configuration and note metadata parsing.

Mitigation: Install PyYAML in a pinned virtual environment before use.

## Reference(s):

- [Todo Accelerator ClawHub page](https://clawhub.ai/liusining/skills/todo-accelerator)
- [Case Study](references/case-study.md)
- [Note YAML Properties](references/note-yaml-properties.md)
- [Processing the work-on-todo Output](references/processing-work-on-todo.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates Markdown Kanban cards, companion Markdown notes, and a YAML configuration file.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
