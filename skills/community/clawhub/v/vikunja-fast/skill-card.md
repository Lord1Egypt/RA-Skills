## Description:

Manage Vikunja projects and tasks (overdue/due/today), mark done, and get quick summaries via the Vikunja API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmigone](https://clawhub.ai/user/tmigone)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to inspect Vikunja projects and tasks, list overdue or due items, and mark selected tasks complete from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials or bearer tokens can be sent to the user-configured Vikunja URL.

Mitigation: Configure only a trusted HTTPS Vikunja URL, use a narrowly scoped token where possible, and rotate credentials if they may have been used over HTTP.

Risk: The done command changes remote task state.

Mitigation: Require explicit user intent and verify the target task ID before running commands that mark tasks complete.

Risk: Username/password fallback increases credential exposure.

Mitigation: Prefer JWT token authentication and avoid username/password fallback unless necessary.

## Reference(s):

- [Vikunja](https://vikunja.io/)
- [Vikunja Filters](https://vikunja.io/docs/filters/)
- [ClawHub skill page](https://clawhub.ai/tmigone/skills/vikunja-fast)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and formatted task summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, VIKUNJA_URL, and either VIKUNJA_TOKEN or username/password credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
