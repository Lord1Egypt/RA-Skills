## Description: <br>
Manage Things 3 via the `things` CLI on macOS, including adding and updating projects and todos through the URL scheme and reading, searching, and listing local Things data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenswj](https://clawhub.ai/user/kenswj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this macOS-only skill to let an agent inspect a local Things 3 database and prepare or run `things` CLI commands for task, project, area, and tag workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local Things 3 data and make task changes through the `things` CLI. <br>
Mitigation: Install only in trusted environments, review proposed changes before writes, and prefer `things --dry-run` previews before modifying tasks. <br>
Risk: The skill depends on an unpinned third-party CLI installed from a Go module. <br>
Mitigation: Review and pin the CLI version where possible, and update it through a controlled dependency process. <br>
Risk: Granting Full Disk Access may expose more local data than the skill needs for normal operation. <br>
Mitigation: Grant Full Disk Access only when database reads fail and only to the calling app that needs it. <br>
Risk: Persisting `THINGS_AUTH_TOKEN` enables ongoing update capability. <br>
Mitigation: Avoid persisting the token unless continuous update access is intentional; prefer passing it only for specific update operations. <br>


## Reference(s): <br>
- [Things Mac on ClawHub](https://clawhub.ai/kenswj/things-mac-1-0-0) <br>
- [things3-cli](https://github.com/ossianhempel/things3-cli) <br>
- [things3-cli Go install module](https://github.com/ossianhempel/things3-cli/cmd/things) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [macOS-only; requires the `things` binary and local Things 3 access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
