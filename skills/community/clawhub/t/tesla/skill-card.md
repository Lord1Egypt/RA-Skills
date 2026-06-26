## Description: <br>
Control Tesla vehicles for lock and unlock, climate, location, charging status, and related vehicle operations with multi-vehicle support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mvanhorn](https://clawhub.ai/user/mvanhorn) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and operators use this skill to query Tesla vehicle status and send remote vehicle commands such as locking, climate control, charging control, location lookup, honking, flashing lights, and wake operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send commands that affect a real vehicle, including unlock, climate, charging, honk, flash, and wake operations. <br>
Mitigation: Install and run it only on trusted machines with trusted operators, and review high-impact commands before execution. <br>
Risk: Vehicle location and status responses can reveal sensitive personal information. <br>
Mitigation: Limit access to the skill and its outputs, and avoid sharing location or status results outside the intended operator context. <br>
Risk: Authentication tokens are cached locally and can grant ongoing account access if exposed. <br>
Mitigation: Treat the Tesla token cache as a password, protect the local account, and remove or rotate cached credentials when access should end. <br>
Risk: Without explicit vehicle selection, commands target the first vehicle on the account. <br>
Mitigation: Prefer explicit vehicle selection for every command when multiple vehicles are available. <br>


## Reference(s): <br>
- [Tesla Fleet API Documentation](https://developer.tesla.com/docs/fleet-api) <br>
- [Unofficial Tesla Owner API Documentation](https://tesla-api.timdorr.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, JSON, Configuration] <br>
**Output Format:** [Plain text command output with optional JSON for status data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may perform Tesla API actions and return status summaries, confirmations, vehicle location links, or structured status data.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
