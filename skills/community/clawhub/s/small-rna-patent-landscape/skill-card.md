## Description:

Builds a company-level small RNA patent landscape from a patent number list, including patent text collection, ASO/siRNA/mRNA/RNA portfolio analysis, XLSX workbooks, technical tagging, and multidimensional HTML timeline dashboards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent analysts, IP teams, and small RNA therapeutics strategy teams use this skill to turn patent publication or application number lists into structured landscape analysis, customer-readable technical tags, strategy worksheets, and an interactive portfolio timeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow writes local patent reports, dashboards, intermediate data, and project scaffold files.

Mitigation: Run it in a dedicated project directory and review generated files before sharing or deploying them.

Risk: Patent fetching may use patent MCP or other tools that can access proprietary patent data.

Mitigation: Review MCP and tool permissions before fetching data, and use only approved data sources for confidential or licensed patent collections.

Risk: Default customer-facing labels are Chinese-oriented and may not match every audience.

Mitigation: Specify a different output language when Chinese labels are not appropriate for the intended readers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuanzhian-patsnap/skills/small-rna-patent-landscape)
- [Small RNA Patent Tag Taxonomy](references/tag-taxonomy.md)
- [Workbook Schema](references/workbook-schema.md)
- [HTML Dashboard Specification](references/html-dashboard.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown patent texts, XLSX workbooks, JSON/CSV intermediate data, standalone HTML dashboards, shell commands, and configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local project folders such as patent_markdowns/ and outputs/patent_analysis/; dashboard and workbook labels may be Chinese-oriented unless the user asks for another output language.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
