## Description:

An MCP server that provides native tools to dynamically search VMware Aria Operations for Logs (Log Insight).

This skill is ready for commercial/non-commercial use.

## Publisher:

[kasture-rohit](https://clawhub.ai/user/kasture-rohit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use this MCP skill to let an agent search VMware Aria Operations for Logs by keyword and inspect recent VCF log events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an API token to fetch raw infrastructure logs that may contain sensitive operational data.

Mitigation: Use a least-privilege read-only Log Insight token and add clear query and redaction controls before exposing returned log data to an agent.

Risk: TLS certificate verification is disabled for Log Insight requests.

Mitigation: Enable certificate verification or install the correct trusted certificate chain before using the skill against sensitive logs.

Risk: Dependencies are not pinned in the artifact requirements.

Mitigation: Pin and review dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kasture-rohit/skills/vcf-loginsight-mcp)
- [Project homepage](https://github.com/kasture-rohit/vcf-openclaw-skills)

## Skill Output:

**Output Type(s):** [Text, Configuration]

**Output Format:** [Plain text log search results or error messages, with JSON MCP server configuration in setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LOGINSIGHT_HOST and LOGINSIGHT_API_TOKEN; the query tool accepts a keyword and an optional event limit.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
