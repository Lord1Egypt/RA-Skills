## Description:

Provides an agent with access to an MCP SSH server for creating SSH sessions, executing commands on authorized remote devices, listing session and command history, checking service health, and closing sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[is-the-king](https://clawhub.ai/user/is-the-king)

### License/Terms of Use:


## Use Case:

Developers, network engineers, and operations teams use this skill to let an agent administer authorized SSH targets through the MCP_Server_Trigger tool interface. It supports session creation, command execution, health checks, active-session listing, historical-session review, command-history review, and session closure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute remote SSH commands on infrastructure targets.

Mitigation: Limit use to authorized hosts, require human review for high-impact commands, and restrict agent access to least-privilege SSH accounts.

Risk: SSH usernames and passwords may be passed as tool parameters.

Mitigation: Avoid reusable production passwords, prefer keys or a secret manager, and prevent credentials from being stored in prompts, logs, or shared transcripts.

Risk: Session and command history may contain sensitive operational data.

Mitigation: Treat history output as sensitive, restrict access to history tools, and align retention with organizational security policy.

Risk: The skill depends on globally installed mcp2skill tooling.

Mitigation: Review and pin the dependency before installation, and update it through a controlled dependency-management process.

## Reference(s):

- [MCP Tools Reference](references/TOOLS.md)
- [mcp2skill](https://github.com/fenwei-dev/mcp2skill)
- [ClawHub Skill Page](https://clawhub.ai/is-the-king/skills/ssh-netmiko)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Text and JSON-like MCP tool responses, with command outputs returned from remote SSH targets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mcp2skill and access to the MCP_Server_Trigger service; SSH credentials, session identifiers, hostnames, device types, ports, and command text may be passed as tool parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
