## Description: <br>
Control and monitor Tesla vehicles via the Tessie API, including status, battery, location, charging, climate, locks, trunks, lights, horn, and software update commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biguntroll](https://clawhub.ai/user/biguntroll) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent monitor and control Tesla vehicles through a Tessie account. It is suited for workflows such as checking charge and location, managing climate or charging, and receiving software update status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Tessie API key allows an agent to read sensitive vehicle status and location data. <br>
Mitigation: Store TESSIE_API_KEY in a secret manager or tightly protected environment and expose it only to trusted agent workflows. <br>
Risk: Vehicle commands can have real-world effects, including unlocking doors, opening trunks, changing charging behavior, climate control, horn, lights, and software updates. <br>
Mitigation: Verify the VIN before commands and require explicit user confirmation before any physical or state-changing action. <br>
Risk: Recurring update checks can run unattended if the optional cron workflow is enabled. <br>
Mitigation: Enable scheduled checks only when recurring Tessie access is intended and review the schedule and notification behavior before deployment. <br>


## Reference(s): <br>
- [Tessie API Reference](references/api.md) <br>
- [Tessie Developer Reference](https://developer.tessie.com/reference) <br>
- [ClawHub Skill Page](https://clawhub.ai/biguntroll/tesla-tessie) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TESSIE_API_KEY and usually a target vehicle VIN.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
