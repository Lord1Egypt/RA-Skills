## Description:

Manage macOS launchd user agents to start, stop, restart, check status, and access logs of persistent background services without sudo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnylambada](https://clawhub.ai/user/johnnylambada)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to manage long-running local macOS processes as user-level launchd services, including installation, removal, status checks, service listing, and log access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can persist arbitrary user commands as macOS launchd services.

Mitigation: Use it only for commands that are intentionally meant to survive beyond the current session, and review the command, arguments, working directory, and environment variables before installation.

Risk: The security scan reports eval and plist-escaping issues that make untrusted input unsafe.

Mitigation: Avoid untrusted service names, commands, arguments, work directories, and environment values until those issues are fixed.

Risk: Environment variables supplied with --env may be written into the generated service configuration.

Mitigation: Do not pass secrets through --env; prefer a safer secret-loading mechanism outside the generated launchd plist.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnnylambada/skills/toolguard-daemon-control)
- [ClawHub publisher profile](https://clawhub.ai/user/johnnylambada)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and shell output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create, load, unload, inspect, and log user-level launchd services when the bundled shell scripts are executed.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
