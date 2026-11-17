## Description:

Runs multiple forward and reverse SSH tunnels across hosts from a plain-text rules file, using key-based authentication and automatic retries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system administrators use the skill to configure and supervise multiple long-lived forward or reverse SSH tunnels across one or more hosts from a single rules file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer is fetched from a changing online source, and the scan did not inspect the downloaded installer.

Mitigation: Use a fixed, trusted version and inspect the installer contents and integrity before installing.

Risk: The setup instructions can append to a shell startup file and source it.

Mitigation: Review the exact command and resulting startup-file change before running it.

Risk: Reverse tunnels can make a local service reachable from the remote host; forward tunnels can expose remote services through the local machine.

Mitigation: Use only trusted hosts and bind tunnels only to the interfaces and ports that need access.

Risk: Rules files reference private keys, and the skill uses those keys to connect to configured hosts.

Mitigation: Keep key files permission-restricted and keep keys and rules files out of world-readable locations and source repositories.

Risk: Each failed connection retries indefinitely, and signaling only the main process may leave SSH child processes running.

Mitigation: Confirm persistent retries are intended and stop the process group or run under a service manager that stops the full control group.

## Reference(s):

- [Setup and configuration reference](references/setup.md)
- [Project homepage](https://github.com/psyb0t/ssh-tunnel-swarm)
- [ClawHub release page](https://clawhub.ai/psyb0t/skills/ssh-tunnel-swarm)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Operational guidance]

**Output Format:** [Plain-text tunnel rules and environment-variable settings used to run SSH tunnel sessions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supervises multiple forward and reverse tunnels with automatic retries until stopped.]

## Skill Version(s):

1.4.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
