## Description: <br>
Provides real-time YouBike 2.0 station lookup for Taipei, New Taipei, and Taoyuan, with nearby search by coordinates and keyword-based station search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dabendan2](https://clawhub.ai/user/dabendan2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this MCP server to retrieve current YouBike station availability in Taipei, New Taipei, and Taoyuan by keyword or nearby coordinates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing npm dependencies can run package lifecycle scripts such as prepare hooks. <br>
Mitigation: Review package scripts before npm install and install in a scoped environment when possible. <br>
Risk: Tool results depend on public YouBike APIs that may be unavailable, delayed, or changed by data providers. <br>
Mitigation: Treat station availability as live external data and verify critical trip decisions against official services. <br>


## Reference(s): <br>
- [Taipei YouBike 2.0 Data Source](https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json) <br>
- [New Taipei YouBike 2.0 Data Source](https://data.ntpc.gov.tw/api/datasets/010e5b15-3823-4b20-b401-b1cf000550c5/json?size=2000) <br>
- [Taoyuan YouBike 2.0 Data Source](https://opendata.tycg.gov.tw/api/v1/dataset.api_access?rid=08274d61-edbe-419d-8fcc-7a643831283d&format=json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API Calls] <br>
**Output Format:** [JSON text returned by MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Station results include station name, city, area, address, bike availability, coordinates, update time, and distance for nearby searches.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and MCP server version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
