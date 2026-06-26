## Description: <br>
Interact with Uptime Kuma monitoring server. Use for checking monitor status, adding/removing monitors, pausing/resuming checks, viewing heartbeat history. Triggers on mentions of Uptime Kuma, server monitoring, uptime checks, or service health monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mSarheed](https://clawhub.ai/user/mSarheed) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations teams use this skill to inspect Uptime Kuma monitor health, create or remove monitors, pause or resume checks, review heartbeat history, and list notification channels from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use stored Uptime Kuma credentials to change monitoring configuration, including deleting monitors or pausing monitoring. <br>
Mitigation: Use a least-privilege Uptime Kuma account where possible, verify monitor IDs before changes, and require human confirmation before delete or pause-all actions. <br>
Risk: The skill depends on the external uptime-kuma-api Python package. <br>
Mitigation: Pin and review the uptime-kuma-api dependency before deployment. <br>


## Reference(s): <br>
- [Uptime Kuma skill page](https://clawhub.ai/mSarheed/uptime-kuma) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Uptime Kuma URL, username, and password environment variables; JSON output is available for several CLI commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
