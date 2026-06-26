## Description: <br>
Manage ThingsBoard devices, dashboards, telemetry, and users via the ThingsBoard REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hoangnv170752](https://clawhub.ai/user/hoangnv170752) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to administer ThingsBoard IoT resources, including devices, telemetry, dashboards, assets, users, and customers through REST API commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes high-impact ThingsBoard administration actions, including telemetry deletion and dashboard publication. <br>
Mitigation: Verify the target tenant, device, dashboard, and keys before execution, and require explicit confirmation before destructive or public-sharing commands. <br>
Risk: Deleting telemetry can remove important operational data. <br>
Mitigation: Back up or export important telemetry before running deletion commands. <br>


## Reference(s): <br>
- [ThingsBoard](https://thingsboard.io) <br>
- [ClawHub skill page](https://clawhub.ai/hoangnv170752/thingsboard-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl and jq with ThingsBoard URL and credential environment variables.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
