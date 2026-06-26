## Description: <br>
Queries and presents current vessel position details from the HiFleet position API for a supplied MMSI after a HiFleet token is configured. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charleiWang](https://clawhub.ai/user/charleiWang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External maritime operations users and agent developers use this skill to look up a vessel by MMSI and return position, heading, speed, destination, and status once a HiFleet token is configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HiFleet token exposure through request URLs or logs. <br>
Mitigation: Configure the token as a secret and avoid logging full request URLs. <br>
Risk: Broad trigger terms may activate this skill in unrelated assistant contexts. <br>
Mitigation: Narrow trigger terms or route only vessel-position queries to this skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/charleiWang/ship-position) <br>
- [HiFleet Position API Endpoint](https://api.hifleet.com/position/position/get/token) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API request examples and JSON response-field descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a valid HiFleet user token and a 9-digit MMSI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
