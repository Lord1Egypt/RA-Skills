## Description:

Local tender search and reporting skill for China's technology procurement market, supporting province and keyword queries, daily or weekly summaries, data-quality checks, and Feishu-oriented report workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yongliw2006](https://clawhub.ai/user/yongliw2006)

### License/Terms of Use:

MIT-0

## Use Case:

External sales teams, system integrators, IT service providers, and managers use this skill to review recent China tender opportunities, filter by province or keyword, generate brief market reports, and decide which bids to pursue.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill requires tender-site cookies and a Feishu webhook URL, which may expose account access or internal channel posting rights if over-privileged credentials are used.

Mitigation: Use dedicated low-privilege tender-site accounts and approved internal webhook channels; rotate or revoke credentials after testing or when access is no longer needed.

Risk: The packaged code does not fully match advertised automated collection and push behavior, so users may rely on capabilities that are not present in the reviewed package.

Mitigation: Treat the package as a local report and search interface unless an installation-specific review confirms the advertised automation and push flow.

Risk: The report command can execute code from a mutable local OpenClaw workspace path outside the reviewed package.

Mitigation: Run report generation only in trusted workspaces and review the external script path before invoking report commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yongliw2006/skills/tender-intelligence)
- [Data Sources Reference](references/data-sources.md)
- [Gansu Cities Reference](references/gansu-cities.md)
- [User Guide](USER_GUIDE.md)
- [Report Sections Specification](docs/SECTIONS.md)
- [Qianlima Tender Platform](https://vip.qianlima.com)
- [Zhongxiang Tender Platform](https://vip.ccpc360.com)
- [Gansu Government Procurement](http://www.ccgp-gansu.gov.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Terminal text and Markdown-style reports with command-line configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and tender-site cookies or Feishu webhook values for workflows that access protected data or push reports.]

## Skill Version(s):

3.2.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
