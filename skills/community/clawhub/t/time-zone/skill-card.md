## Description:

一个全面的MCP服务器，提供全球时区管理和时间转换功能，适用于全球业务协调、旅行规划和开发运维。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operations teams, travel planners, and global business coordinators use this skill to get current times for named time zones and convert a specified time between source and target time zones.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user API key may be stored in a local plaintext .env file.

Mitigation: Use the skill only in a trusted, private workspace; keep .env out of source control and prefer safer secret storage before broader deployment.

Risk: Tool calls forward requests to a configurable remote Xiaobenyang endpoint.

Mitigation: Confirm the configured base URL and trust boundary before use, and restrict changes to the endpoint configuration.

Risk: Stale Gaokao references create ambiguity about the skill's intended service and data flow.

Mitigation: Review the skill documentation and package contents before installation, and prefer a version with stale references removed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/time-zone)
- [Xiaobenyang service](https://xiaobenyang.com)
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Configuration guidance]

**Output Format:** [Markdown summary of JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Xiaobenyang API key before tool calls can be made.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
