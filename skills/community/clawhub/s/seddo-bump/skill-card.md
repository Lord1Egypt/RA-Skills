## Description: <br>
Coordinate a swarm of AI agents across machines using a private GitHub Gist as a shared communication bus with a hub-and-spoke fork model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dofbi](https://clawhub.ai/user/dofbi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent operators use Seddo to coordinate agents running on different machines or GitHub accounts. The skill helps agents share tasks, messages, lessons, status, and completion updates through GitHub Gist workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared Gist coordination data can expose sensitive tasks, messages, gist URLs, or join tokens if handled carelessly. <br>
Mitigation: Treat gist URLs and join tokens as secrets, avoid putting client data or credentials in shared messages or tasks, and delete old gists when a seddo ends. <br>
Risk: The skill requires GitHub authentication and gist permissions, which can increase credential exposure if long-lived tokens are exported into shells or logs. <br>
Mitigation: Prefer GitHub CLI credential storage, use the minimum required gist scope, and revoke or rotate old tokens after use. <br>
Risk: Remote installer or shell scripts can execute local commands during setup. <br>
Mitigation: Review the installer and seddo shell script before running them, especially in workspaces that contain sensitive files. <br>
Risk: Concurrent edits to Gist-backed files can overwrite or obscure coordination updates. <br>
Mitigation: Sync before writing, append rather than replace shared records, avoid simultaneous edits to the same file, and use the documented lock marker during contention. <br>


## Reference(s): <br>
- [Seddo Bump on ClawHub](https://clawhub.ai/dofbi/seddo-bump) <br>
- [Publisher profile](https://clawhub.ai/user/dofbi) <br>
- [README.md](README.md) <br>
- [OpenCode installation guide](OPENCODE.md) <br>
- [Agent participation guide](AGENTS.md) <br>
- [OpenCode configuration schema](https://opencode.ai/config.json) <br>
- [GitHub token settings](https://github.com/settings/tokens) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance, shell command output, and GitHub Gist coordination files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Seddo configuration and shared Gist files for messages, tasks, lessons, roster, registry, and activity logs.] <br>

## Skill Version(s): <br>
2.6.6 (source: server release metadata and scripts/seddo.sh) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
