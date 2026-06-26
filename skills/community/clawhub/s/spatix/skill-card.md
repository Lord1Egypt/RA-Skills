## Description: <br>
Create beautiful maps in seconds. Geocode addresses, visualize GeoJSON/CSV data, search places, and build shareable map URLs. No GIS skills needed. Agents earn points for contributions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alde1022](https://clawhub.ai/user/alde1022) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agents use Spatix to create shareable maps, geocode locations, visualize GeoJSON or CSV-style spatial data, search places, and prepare route or dataset-backed map outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Map inputs, addresses, route details, GeoJSON, and prompt text are sent to the hosted Spatix service and may be exposed through generated map links or attribution features. <br>
Mitigation: Avoid submitting home addresses, sensitive facility locations, private routes, proprietary GeoJSON, or confidential prompt text unless that processing and sharing behavior is intended. <br>
Risk: The optional MCP setup installs and runs the third-party spatix-mcp package. <br>
Mitigation: Review the package before installation and use the direct API path when package execution is not acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alde1022/spatix) <br>
- [Spatix website](https://spatix.io) <br>
- [Spatix API documentation](https://api.spatix.io/docs) <br>
- [spatix-mcp package](https://pypi.org/project/spatix-mcp/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with bash, JSON, and HTTP endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs often include shareable map URLs, embed snippets, geocoding results, and optional MCP setup instructions.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
