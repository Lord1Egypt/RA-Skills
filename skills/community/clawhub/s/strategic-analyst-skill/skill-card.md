## Description:

Provides McKinsey-style industry and market analysis using classic strategic frameworks, live public-source research, data provenance logs, and Markdown or HTML report outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yamaz49](https://clawhub.ai/user/yamaz49)

### License/Terms of Use:

MIT-0

## Use Case:

Executives, investors, students, and market entrants use this skill to structure industry research, market sizing, competitive analysis, market-entry assessment, and investment-support analysis with cited public data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics and source queries may be sent to web or search providers.

Mitigation: Use the skill only for topics approved for external search, and avoid confidential strategy, acquisition, investment, customer, or non-public data unless provider use is explicitly controlled.

Risk: The skill keeps a raw data collection log containing search queries, URLs, source snippets, and timestamps.

Mitigation: Review storage location and retention for generated data_collection.md files, and remove sensitive prompts or source excerpts before sharing reports.

Risk: Generated HTML reports may include untrusted content and links.

Mitigation: Review generated HTML before opening or sharing it, escape or sanitize converted content, and validate links from untrusted inputs.

Risk: Runtime setup can depend on external components such as MCP search services and npx-installed packages.

Mitigation: Prefer pinned, reviewed dependency versions and approved MCP server configuration before using the skill in production workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yamaz49/skills/strategic-analyst-skill)
- [Skill Instructions](artifact/SKILL.md)
- [Skill Configuration](artifact/skill.yaml)
- [Data Provenance Template](artifact/templates/data_provenance.md)
- [Report Reading Guide](artifact/docs/how_to_read_report.md)
- [HTML Report Style Guide](artifact/docs/html_style_guide.md)
- [Visualization Standards](artifact/docs/visualization_standards.md)
- [Tavily](https://tavily.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, HTML reports, data provenance logs, tables, configuration snippets, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires sourced data links and credibility ratings for key market, growth, and competitive data; HTML reports may include table download controls.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
