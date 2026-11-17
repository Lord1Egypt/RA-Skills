## Description:

Tencent Map helps agents use Tencent Maps WebService APIs for geocoding, place search, route planning, IP location, and WeChat Mini-Program LBS integration guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangifonly](https://clawhub.ai/user/zhangifonly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query Tencent Maps WebService endpoints, troubleshoot WeChat Mini-Program location-service integrations, and avoid common Tencent coordinate-order and key-configuration mistakes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Map queries, route endpoints, IP addresses, or location inputs may be sent to Tencent's apis.map.qq.com service.

Mitigation: Use the skill only when sharing those locations with Tencent is acceptable, and avoid sensitive locations unless that third-party data sharing has been approved.

Risk: The bundled CLI requires a Tencent Maps WebService API key through QQMAP_KEY.

Mitigation: Provide only an appropriate Tencent Maps key, keep it out of committed files and chat transcripts, and rotate it if it is exposed.

Risk: Tencent uses lat,lng coordinate order, which can be confused with lng,lat conventions from other map providers.

Mitigation: Check coordinate order before routing or geocoding workflows, especially when migrating data from another map platform.

## Reference(s):

- [Tencent Maps WebService API endpoint](https://apis.map.qq.com)
- [ClawHub skill page](https://clawhub.ai/zhangifonly/skills/tencent-map)
- [ClawHub publisher profile](https://clawhub.ai/user/zhangifonly)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses from the bundled CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Tencent's apis.map.qq.com service when the agent runs the bundled CLI with QQMAP_KEY.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
