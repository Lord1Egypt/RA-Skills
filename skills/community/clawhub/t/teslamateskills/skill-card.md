## Description: <br>
Query TeslaMate vehicle data via Grafana API for vehicle status, battery information, drives, charges, statistics, driving score, battery health, and trip data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zengfei88](https://clawhub.ai/user/zengfei88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and TeslaMate users use this skill to query a Grafana-backed TeslaMate PostgreSQL datasource for vehicle telemetry, trip history, charging statistics, efficiency trends, alerts, and route estimates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location and route features can expose precise vehicle coordinates or destination addresses to public map services. <br>
Mitigation: Avoid address, route, drive-address, and location features unless the user accepts that exposure, or modify the skill to use trusted self-hosted geocoding and routing services. <br>
Risk: The skill can access TeslaMate vehicle telemetry through Grafana. <br>
Mitigation: Keep Grafana private and read-only, and verify the workspace configuration points only to the user's intended Grafana instance. <br>


## Reference(s): <br>
- [TeslaMate Database Schema](artifact/references/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text and terminal tables, with Markdown command examples in documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are based on Grafana API responses and may include vehicle telemetry, locations, route estimates, charging statistics, and status summaries.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
