## Description:

Query traffic data, including real-time road conditions, traffic incidents, and SCATS intersection data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teweitao](https://clawhub.ai/user/teweitao)

### License/Terms of Use:


## Use Case:

Developers and traffic operations users can use this skill to query road conditions, traffic incidents, and SCATS intersection status through configured map and SCATS API credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses named map and SCATS API keys and can make outbound requests to external traffic data providers.

Mitigation: Install only where use of those credentials and provider requests is acceptable; use scoped keys and review provider access before production use.

Risk: The security guidance notes missing or incorrect command documentation and dependency cleanup needs.

Mitigation: Review and correct the command documentation, document the config command, and audit or pin HTTP dependencies before production use.

Risk: SCATS querying is documented, but artifact behavior reports that the SCATS API call is not implemented yet.

Mitigation: Treat SCATS output as unavailable until the implementation is completed and tested against the intended SCATS provider.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teweitao/skills/traffic-data)
- [Baidu Map Open Platform](https://lbsyun.baidu.com/)
- [Gaode Map Open Platform](https://lbs.amap.com/)
- [Gaode traffic road status endpoint](https://restapi.amap.com/v3/trafficstatus/road)
- [Gaode traffic status endpoint](https://restapi.amap.com/v3/trafficstatus/status)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text CLI output with JSON API responses when provider calls succeed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node and relevant BAIDU_MAP_KEY, GAODE_MAP_KEY, or SCATS_API_KEY environment variables.]

## Skill Version(s):

1.0.0 (source: package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
