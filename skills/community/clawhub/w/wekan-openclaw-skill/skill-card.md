## Description: <br>
Manage a self-hosted Trello-like board via `wekancli`, including creating, moving, and archiving cards, lists, and boards on a WeKan server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[madsmith](https://clawhub.ai/user/madsmith) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and team agents use this skill to work with self-hosted WeKan task boards through the `wekancli` command-line tool. It is suited for listing board data and creating, moving, archiving, restoring, or deleting board items when the configured WeKan account has the required permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and relies on an external `wekancli` dependency from GitHub. <br>
Mitigation: Install it only when the upstream `wekan-cli` dependency is trusted. <br>
Risk: `WEKAN_TOKEN` is a bearer secret for a live WeKan account. <br>
Mitigation: Protect the token and use a dedicated least-privilege WeKan account instead of an admin token for normal board work. <br>
Risk: Archive, restore, delete, and user-listing operations can mutate live board data or require elevated permissions. <br>
Mitigation: Require explicit confirmation before those operations and reserve admin-capable tokens for tasks that need them. <br>


## Reference(s): <br>
- [Wekan skill page](https://clawhub.ai/madsmith/wekan-openclaw-skill) <br>
- [wekan-cli GitHub dependency](https://github.com/madsmith/wekan_cli.git) <br>
- [CLI examples](references/cli-examples.md) <br>
- [User installation notes](references/user-install.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires `wekancli`, `WEKAN_URL`, and `WEKAN_TOKEN`; command effects depend on the configured WeKan user's permissions.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
