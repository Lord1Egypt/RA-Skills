## Description:

Track how a brand shows up in AI answers, and act on the findings, through Shruwd's MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilpr](https://clawhub.ai/user/ilpr)

### License/Terms of Use:

MIT-0

## Use Case:

Brand and marketing teams use this skill to set up visibility tracking, compare competitors, and review how their brand appears in AI answers and crawler activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting the skill grants access to a Shruwd workspace; write access can change tracked brands and start measurements.

Mitigation: Use read-only OAuth for reporting, and grant write access or an API key only when changes are intended.

Risk: Incomplete measurements or small samples can lead to misleading visibility reports.

Mitigation: Wait for the measurement cycle to close and report intervals and sample sizes; do not treat insufficient data as zero.

## Reference(s):

- [Shruwd](https://shruwd.io)
- [Shruwd MCP documentation](https://shruwd.io/docs/api/mcp-server)
- [Shruwd machine-readable documentation](https://shruwd.io/llms.txt)
- [Shruwd pricing and account information](https://shruwd.io/pricing)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Configuration instructions]

**Output Format:** [Text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include per-engine visibility, confidence intervals, sample sizes, and crawler activity.]

## Skill Version(s):

1.0.3 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
