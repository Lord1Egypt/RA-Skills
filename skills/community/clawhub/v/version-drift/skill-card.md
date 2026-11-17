## Description:

One command to check if your entire stack is up to date. SSHes into servers, queries APIs, and compares installed versions against latest — across every service you run.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rtaylorgraham](https://clawhub.ai/user/rtaylorgraham)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Version Drift to compare installed versions on local machines, SSH hosts, services, and containers against upstream release sources, then produce reports for maintenance planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured SSH checks can run powerful commands on remote hosts, including examples using root.

Mitigation: Use a dedicated unprivileged SSH account, avoid root, and limit configured commands to read-only version checks.

Risk: HTTP checks may send API tokens to service endpoints, and examples include an HTTP URL with an Authorization header.

Mitigation: Require HTTPS for requests carrying tokens, keep SSL verification enabled, and store tokens in environment variables instead of config files.

Risk: The tool executes local shell commands from its config file.

Mitigation: Restrict write access to the config file and review changes before running checks on real infrastructure.

## Reference(s):

- [ClawHub: Version Drift](https://clawhub.ai/rtaylorgraham/skills/version-drift)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Terminal table, JSON, or Markdown report; optional generated Docker Compose check configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads a user-provided YAML or JSON config and may persist drift history in a state file.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
