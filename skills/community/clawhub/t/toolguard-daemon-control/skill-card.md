## Description: <br>
Manage macOS launchd user agents to start, stop, restart, check status, and access logs of persistent background services without sudo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnnylambada](https://clawhub.ai/user/johnnylambada) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to install, inspect, and remove persistent macOS launchd user agents for processes that should continue beyond an agent session. It is intended for service lifecycle operations, including launchd plist creation, status checks, and log access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can immediately create persistent, auto-restarting macOS launchd services. <br>
Mitigation: Review the exact command, arguments, working directory, and environment values before installing a service. <br>
Risk: The server security summary reports unsafe input handling in the installer. <br>
Mitigation: Prefer a patched version that removes eval, validates service names and environment keys, escapes plist XML, and asks for confirmation before loading persistent services. <br>
Risk: Environment variables passed with --env may expose sensitive values through service configuration. <br>
Mitigation: Do not pass secrets through --env. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johnnylambada/toolguard-daemon-control) <br>
- [Publisher profile](https://clawhub.ai/user/johnnylambada) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces launchd service-management instructions and uses user-level plist and log paths on macOS.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
