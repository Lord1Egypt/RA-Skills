## Description:

Provides real-time YouBike 2.0 station status lookup for Taipei, New Taipei, and Taoyuan, with nearby coordinate search and keyword search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dabendan2](https://clawhub.ai/user/dabendan2)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this MCP server to retrieve current YouBike station availability by station keyword or by proximity to a latitude and longitude in Taipei, New Taipei, or Taoyuan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP server makes outbound requests to public YouBike data APIs.

Mitigation: Deploy only in environments where outbound access to the listed public data feeds is acceptable.

Risk: Dependency hygiene is the primary security concern identified by the release scan.

Mitigation: Pin or update Node dependencies to patched versions before broad deployment.

Risk: The package includes a husky prepare script that is not needed for normal runtime use.

Mitigation: Review published package scripts and remove development-only lifecycle behavior before broad deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dabendan2/skills/youbike-mcp)
- [Taipei YouBike 2.0 real-time data feed](https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json)
- [New Taipei YouBike 2.0 data feed](https://data.ntpc.gov.tw/api/datasets/010e5b15-3823-4b20-b401-b1cf000550c5/json?size=2000)
- [Taoyuan YouBike 2.0 data feed](https://opendata.tycg.gov.tw/api/v1/dataset.api_access?rid=08274d61-edbe-419d-8fcc-7a643831283d&format=json)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON text returned through MCP tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Station results include availability counts, location fields, update time, and distance for nearby searches.]

## Skill Version(s):

1.0.2 (source: server release evidence and MCP server metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
