## Description:

Manage TickTick tasks and projects via the `ttg` CLI, including task CRUD, checklists and subtasks, reminders, recurring tasks, search, tags, natural-language due dates, and JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dhruvkelawala](https://clawhub.ai/user/dhruvkelawala)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and productivity-focused users use this skill to have an agent create, list, edit, search, complete, and delete TickTick tasks and related project, tag, reminder, recurrence, and checklist data through the `ttg` command-line interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer runs unpinned code from an external GitHub repository.

Mitigation: Review the installer before use and prefer installing `ttg` from a pinned, reviewed release or commit without elevated privileges.

Risk: TickTick API credentials are stored in `~/.config/ttg/config.json`.

Mitigation: Store the credentials file with owner-only permissions and avoid sharing logs or outputs that may expose configuration details.

Risk: The skill can modify or remove TickTick tasks and checklist items.

Mitigation: Review proposed edit, completion, and delete commands before execution, especially for shared or business-critical task lists.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dhruvkelawala/skills/ticktick-go)
- [ttg CLI repository referenced by the skill](https://github.com/dhruvkelawala/ticktick-go)
- [TickTick](https://ticktick.com)
- [TickTick developer credentials](https://developer.ticktick.com/manage)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-oriented command examples for scripting with `ttg`.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
