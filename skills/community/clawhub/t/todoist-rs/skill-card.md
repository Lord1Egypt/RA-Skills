## Description:

Manage Todoist tasks through the td CLI for listing, creating, completing, editing, deleting, and syncing tasks in a Todoist account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luoandorder](https://clawhub.ai/user/luoandorder)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to manage a Todoist account from natural-language task requests by proposing or running td CLI commands for task, project, label, and sync operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, edit, complete, reopen, or delete live Todoist tasks.

Mitigation: Use explicit Todoist wording for write actions and review proposed write or delete commands before execution.

Risk: The documented installation paths use unpinned third-party Homebrew and Cargo sources.

Mitigation: Install only after trusting the publisher and prefer a pinned, reviewed CLI version when available.

Risk: Task reads can use a local cache and may be stale.

Mitigation: Run td sync or use --sync before actions that depend on current Todoist state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luoandorder/skills/todoist-rs)
- [Publisher profile](https://clawhub.ai/user/luoandorder)
- [todoist-rs project homepage](https://github.com/LuoAndOrder/todoist-rs)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Todoist CLI commands that read from cache, sync task state, or modify live Todoist account data.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
