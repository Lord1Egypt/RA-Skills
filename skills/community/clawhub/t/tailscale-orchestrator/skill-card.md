## Description: <br>
Manage and monitor a Tailscale network from ClawBot by using the local Tailscale CLI to check status and list connected devices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sahil1005](https://clawhub.ai/user/sahil1005) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to inspect Tailscale connection status and connected device details from an agent session without embedding Tailscale API keys in the skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reveal Tailscale device names, Tailscale IP addresses, and online status in chat or logs. <br>
Mitigation: Use it only in agent sessions and logging environments where exposing tailnet inventory details is acceptable. <br>
Risk: Future releases could add commands that change network settings, expose services, share devices, or approve access. <br>
Mitigation: Re-review security findings and behavior before installing or upgrading to a future version. <br>
Risk: The skill depends on the host Tailscale CLI and the permissions of the user running ClawBot. <br>
Mitigation: Install and configure the Tailscale CLI on a trusted host and run ClawBot with only the permissions needed for status inspection. <br>


## Reference(s): <br>
- [Tailscale CLI Download](https://tailscale.com/download) <br>
- [ClawHub Skill Page](https://clawhub.ai/sahil1005/tailscale-orchestrator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Plain text summaries and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Tailscale CLI to be installed, configured, and available on the host PATH.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
