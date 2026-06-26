## Description: <br>
Windy Access helps an agent run the Windy onboarding CLI to connect supported runtimes to Windy Mail, Windy Chat, Windy Mind, and optional Eternitas identity credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sneakyfree](https://clawhub.ai/user/sneakyfree) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when they want to pair OpenClaw, Hermes Agent, Claude Code, or a generic local runtime with Windy services and manage connection, status, refresh, and disconnect flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to install and run a third-party onboarding CLI that can write credential files across multiple local runtimes. <br>
Mitigation: Install only when the user explicitly wants Windy integration, prefer a pinned auditable package install, and review the CLI source and file changes before running connect. <br>
Risk: The curl-to-shell installer path can execute remote code before review. <br>
Mitigation: Prefer pipx install windy-connect or another pinned package source, and use windy disconnect to remove local Windy configuration when the integration is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sneakyfree/windy-access) <br>
- [Windy Connect Project Homepage](https://github.com/sneakyfree/windy-connect) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke the Windy CLI to install, connect, refresh, status-check, and disconnect local credentials.] <br>

## Skill Version(s): <br>
0.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
