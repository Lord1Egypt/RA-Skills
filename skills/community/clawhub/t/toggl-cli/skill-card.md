## Description:

Control a Toggl Track workspace from the command line to manage time entries, projects, clients, tasks, tags, workspaces, organizations, groups, and user profile data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[froemic](https://clawhub.ai/user/froemic)

### License/Terms of Use:


## Use Case:

Developers, operators, and agent users use this skill to start and stop Toggl timers, inspect or edit time tracking records, and manage related Toggl Track workspace resources from CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install flow asks users to clone, build, and globally link unpinned third-party code.

Mitigation: Install only after reviewing the referenced repository and pinning a specific trusted commit.

Risk: The Toggl API token may be exposed if stored in broad shell environments or shared logs.

Mitigation: Keep TOGGL_API_TOKEN in a narrowly scoped environment file, avoid echoing it, and revoke the token if exposure is suspected.

Risk: Delete commands can remove Toggl resources when the wrong ID is supplied.

Mitigation: Verify workspace and resource IDs before running delete commands, especially in shared or production workspaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/froemic/skills/toggl-cli)
- [Toggl CLI repository linked by artifact](https://github.com/FroeMic/toggl-cli)
- [Toggl Track profile settings](https://track.toggl.com/profile)
- [Toggl Track API v9 base URL](https://api.track.toggl.com/api/v9)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with bash and curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced CLI can return JSON, table, or CSV output for list and get commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
