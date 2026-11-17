## Description:

Controls Nest and Google Home smart home devices via the Starling Home Hub's local REST API, including thermostats, cameras, Nest Protects, Nest x Yale locks, temperature sensors, home/away control, and Nest weather service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaeljmoody](https://clawhub.ai/user/michaeljmoody)

### License/Terms of Use:


## Use Case:

External users, developers, and smart-home operators use this skill to inspect and control Nest and Google Home devices through a local Starling Home Hub, including reading device status, adjusting thermostats, retrieving camera snapshots, and changing lock or home/away state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read camera data and change physical smart-home state, including locks.

Mitigation: Use narrowly scoped API keys, prefer read-only permissions unless writes are required, review commands before execution, and avoid passing untrusted values to set or stream-start operations.

Risk: Weak transport choices can expose API keys or device data on the local network.

Mitigation: Use HTTPS, avoid --http, pin the hub certificate with --cacert where possible, keep the hub address local and verified, and never port-forward hub API ports to the internet.

Risk: The Starling API key is required as a URL query parameter and can be exposed in logs or process-visible command arguments.

Mitigation: Provide the key through STARLING_API_KEY, do not pass keys via --key, avoid storing keys in version-controlled files, and protect any local .env file with restricted permissions.

Risk: Camera snapshots may contain sensitive imagery.

Mitigation: Store snapshots only in owner-readable locations, preserve the script's restrictive file permissions, and delete temporary snapshots when no longer needed.

## Reference(s):

- [Starling Home Hub](https://starlinghome.io)
- [Starling Home Hub Developer Connect API Reference](references/api-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/michaeljmoody/skills/starling-home-hub)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May retrieve sensitive smart-home status, camera snapshots, stream metadata, and command results from a local Starling Home Hub.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
