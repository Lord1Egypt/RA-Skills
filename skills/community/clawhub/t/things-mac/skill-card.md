## Description: <br>
Manage Things 3 via the `things` CLI on macOS (add/update projects+todos via URL scheme; read/search/list from the local Things database). Use when a user asks Clawdbot to add a task to Things, list inbox/today/upcoming, search tasks, or inspect projects/areas/tags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent inspect, search, create, and update Things 3 tasks on macOS through the `things` CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Granting broad macOS Full Disk Access can expose more local data than the skill needs for a specific task. <br>
Mitigation: Try read operations first, grant Full Disk Access only to the intended calling app when required, and revoke access when it is no longer needed. <br>
Risk: Write and update commands can change Things 3 tasks, projects, tags, or completion state. <br>
Mitigation: Use `things --dry-run` before uncertain add or update commands and review the proposed action before execution. <br>
Risk: A Things auth token can authorize update operations if exposed. <br>
Mitigation: Keep `THINGS_AUTH_TOKEN` private and avoid placing token values directly in shared prompts, logs, or reusable command snippets. <br>


## Reference(s): <br>
- [Things Mac ClawHub Page](https://clawhub.ai/steipete/things-mac) <br>
- [things3-cli GitHub Repository](https://github.com/ossianhempel/things3-cli) <br>
- [things3-cli Go Install Module](https://github.com/ossianhempel/things3-cli/cmd/things) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dry-run command previews and guidance for macOS permissions, local Things database access, and Things URL-scheme writes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
