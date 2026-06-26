## Description: <br>
Helps agents control Sonos on the same LAN through ZoneFoundry `zf`, covering readiness checks, playback, queues, service linking, and recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kisssam6886](https://clawhub.ai/user/kisssam6886) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate a local Sonos system through the ZoneFoundry `zf` CLI, including first-run readiness checks, playback, queue management, service readiness, announcements, and recovery on a same-LAN node. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to update the local ZoneFoundry runtime or follow runtime-suggested next commands automatically. <br>
Mitigation: Require user confirmation before runtime updates, service-linking commands, runtime-suggested next commands, and queue pruning; prefer a pinned `zf` version for reproducible deployments. <br>
Risk: The skill controls Sonos devices on the user's local network through the `zf` runtime. <br>
Mitigation: Install only when the user trusts the ZoneFoundry runtime and the local machine is expected to control the Sonos system; review `zf` responses before allowing automatic action. <br>


## Reference(s): <br>
- [ZoneFoundry repository](https://github.com/kisssam6886/zonefoundry) <br>
- [Command Map](references/command-map.md) <br>
- [Onboarding Boundary](references/onboarding-boundary.md) <br>
- [China Service Readiness Notes](references/china-service-linking.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented command output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent to run `zf` locally, prefer structured JSON outputs, and explain results in the user's language.] <br>

## Skill Version(s): <br>
1.5.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
