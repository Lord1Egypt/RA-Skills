## Description:

Manage TickTick tasks and projects from the command line with OAuth2 auth, batch operations, and rate limit handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[norickkevorkov](https://clawhub.ai/user/norickkevorkov)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to authenticate with TickTick, inspect projects and tasks, and create, update, complete, or abandon tasks from shell workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI requests TickTick tasks:read and tasks:write access.

Mitigation: Install only when task read and write access is acceptable for the intended TickTick account.

Risk: OAuth client secrets and tokens are stored in ~/.clawdbot/credentials/ticktick-cli/config.json.

Mitigation: Treat the config file as sensitive and exclude it from shared backups, sync folders, terminals, and logs.

Risk: The batch-abandon command can change multiple tasks without a separate confirmation step.

Mitigation: Review task IDs carefully and prefer listing tasks with --json before running batch-abandon.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/norickkevorkov/skills/ticktick-cli)
- [TickTick Developer Center](https://developer.ticktick.com/manage)
- [TickTick Open API v1](https://developer.ticktick.com/api)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands; CLI commands can return JSON with --json.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TickTick OAuth credentials and stores tokens in a local config file.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact package.json reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
