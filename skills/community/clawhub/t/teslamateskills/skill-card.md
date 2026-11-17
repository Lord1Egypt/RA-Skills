## Description:

Query TeslaMate vehicle data through the Grafana API for vehicle status, battery, drive, charging, route, statistics, driving score, battery health, and trip information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengfei88](https://clawhub.ai/user/zengfei88)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and TeslaMate users use this skill to query Grafana-backed Tesla vehicle status, trip, charging, location, route, efficiency, cost, and battery health data from an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exact vehicle locations or route destinations may be sent to external geocoding or routing services.

Mitigation: Use self-hosted or HTTPS-validated geocoding and routing services, or avoid the location and route features when location sharing is not acceptable.

Risk: Grafana raw SQL access can expose sensitive TeslaMate data if the datasource has broad permissions.

Mitigation: Use a read-only, least-privilege Grafana datasource account and avoid raw-SQL fallback behavior.

## Reference(s):

- [TeslaMate Database Schema](references/schema.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured TeslaMate Grafana PostgreSQL datasource; location and route features may call external geocoding or routing services.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
