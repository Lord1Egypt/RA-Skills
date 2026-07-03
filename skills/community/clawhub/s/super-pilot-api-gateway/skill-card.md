## Description: <br>
Helps agents expose local APIs to the Pilot Protocol network for remote access without placing the API directly on the public internet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[molexazwo](https://clawhub.ai/user/molexazwo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure pilotctl gateway and messaging commands for private API exposure or agent-service integration. It is intended for local API services that should be reachable by authorized Pilot agents rather than exposed as already-public APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote exposure of local APIs can make sensitive services reachable beyond the local machine. <br>
Mitigation: Only map intended endpoints, require authentication, and avoid exposing admin panels, metadata endpoints, private business APIs, or unauthenticated services. <br>
Risk: Gateway and daemon access boundaries may be unclear to users who are unfamiliar with Pilot Protocol networking. <br>
Mitigation: Verify who can reach the service before use, limit allowed endpoints, and stop the daemon when the gateway is no longer needed. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/molexazwo/skills/super-pilot-api-gateway) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the pilot-protocol skill, pilotctl on PATH, a running Pilot daemon, and a local API server.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact _meta.json agrees) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
