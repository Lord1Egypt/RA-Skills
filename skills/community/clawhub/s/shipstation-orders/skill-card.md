## Description: <br>
Monitor ShipStation orders, detect issues, and send alerts for e-commerce businesses using ShipStation across multiple marketplaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cprice70](https://clawhub.ai/user/cprice70) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External e-commerce operators and their agents use this skill to monitor ShipStation order activity, identify new orders, flag stuck or on-hold orders, and surface expedited shipping needs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ShipStation credentials and order or customer details may be exposed if .env or generated state files are committed, backed up broadly, or shared. <br>
Mitigation: Install only in a workspace appropriate for sensitive order data, keep .env, state.json, and shipping-state.json out of source control and broad backups, and restrict access to the workspace. <br>
Risk: Continuous heartbeat or cron monitoring may send order alerts more widely than intended. <br>
Mitigation: Enable scheduled monitoring only when continuous checks are intended and limit alert destinations to approved recipients. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cprice70/shipstation-orders) <br>
- [ShipStation API V1 documentation](https://www.shipstation.com/docs/api/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON from monitoring scripts plus Markdown setup guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node plus SHIPSTATION_API_KEY and SHIPSTATION_API_SECRET; writes local state files to suppress duplicate alerts.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
