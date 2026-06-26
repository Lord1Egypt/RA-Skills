## Description: <br>
Query traffic data - real-time road conditions, traffic incidents, SCATS intersection data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TEweitao](https://clawhub.ai/user/TEweitao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to query road conditions, traffic incidents, and SCATS intersection data from configured traffic data providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Traffic lookups require map-provider or SCATS API keys. <br>
Mitigation: Use restricted API keys with quotas and avoid exposing keys in logs, shared files, or public environments. <br>
Risk: The package documentation references helper scripts that are not present in the artifact. <br>
Mitigation: Verify the installed entry command and prefer the included index.js command interface before operational use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/TEweitao/traffic-data) <br>
- [Baidu Maps Open Platform](https://lbsyun.baidu.com/) <br>
- [Gaode Maps Open Platform](https://lbs.amap.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Console text with JSON API responses and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and provider API keys via BAIDU_MAP_KEY, GAODE_MAP_KEY, or SCATS_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
