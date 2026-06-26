## Description: <br>
Helps manage macOS service persistence and restart recovery using LaunchAgent, tmux bootstrap scripts, wrapper daemons, and service registry updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darwin7381](https://clawhub.ai/user/darwin7381) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add, upgrade, diagnose, and restore persistent macOS services across LaunchAgent, tmux bootstrap, and wrapper-daemon patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact is designed for login-time and crash-recovery persistence on macOS. <br>
Mitigation: Review every LaunchAgent and shell script before loading it, and install only when persistent service recovery is intended. <br>
Risk: The included Claude Telegram wrapper uses permission-bypass flags and auto-confirms trust prompts. <br>
Mitigation: Remove permission-bypass flags and require manual trust confirmation before deployment. <br>
Risk: Bundled scripts contain user-specific paths and service definitions. <br>
Mitigation: Replace hardcoded paths and service entries with values for the target machine before use. <br>
Risk: Some development services may bind to externally reachable interfaces. <br>
Mitigation: Bind development servers to localhost unless remote access is explicitly required. <br>


## Reference(s): <br>
- [Service Persistence Release Page](https://clawhub.ai/darwin7381/service-persistence) <br>
- [Bootstrap Script Template](references/bootstrap-template.md) <br>
- [LaunchAgent plist Template](references/launchagent-template.md) <br>
- [Service Registry Specification](references/registry-spec.md) <br>
- [Wrapper Daemon Script Template](references/wrapper-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON registry entries, plist templates, and shell script snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persistent macOS LaunchAgents, tmux sessions, service registry updates, and wrapper daemons.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
