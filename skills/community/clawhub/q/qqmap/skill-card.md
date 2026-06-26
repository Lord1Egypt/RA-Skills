## Description: <br>
腾讯地图Web服务API集成，用于地点搜索、路线规划、逆地理编码等功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coreyleung-art](https://clawhub.ai/user/coreyleung-art) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to call Tencent Maps Web Service APIs for place search, geocoding, reverse geocoding, and nearby POI lookup. It returns structured JSON for downstream processing or agent responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Map searches, addresses, and coordinates are sent to Tencent Maps under the user's API key. <br>
Mitigation: Avoid submitting highly sensitive personal or confidential locations, and confirm Tencent Maps terms are acceptable for the intended use. <br>
Risk: The Tencent Maps API key can consume quota or expose account access if reused broadly. <br>
Mitigation: Use a restricted API key where possible, keep it in the TENCENT_MAP_KEY environment variable, and monitor quota usage. <br>
Risk: The route command is documented, but server security guidance says to treat it as unavailable until implemented. <br>
Mitigation: Use the implemented search, geocode, reverse_geocode, and around commands, and verify route behavior before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/coreyleung-art/qqmap) <br>
- [Tencent Location Service console](https://lbs.qq.com/dev/console/application/) <br>
- [Tencent Maps Web API endpoint](https://apis.map.qq.com/ws) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Configuration instructions] <br>
**Output Format:** [JSON responses from shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, python3, network access, and the TENCENT_MAP_KEY environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
