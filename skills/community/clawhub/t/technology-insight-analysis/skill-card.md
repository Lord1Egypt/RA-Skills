## Description:

面向任意技术领域的竞争技术洞察分析。输入已检索、筛选、标引的专利数据，自动执行技术路线分析、竞争格局评估、战略机会识别，生成管理层可读的 HTML 可视化洞察报告。适用于固态电池、半导体、生物医药、新能源、化工等任意技术赛道的专利竞争分析与技术白皮书生成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent analysts, R&D strategy teams, and business decision makers use this skill to turn already retrieved, screened, and tagged patent datasets into evidence-based technology route analysis, competitive landscape assessment, strategic opportunity findings, and management-ready Markdown or HTML reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The advertised broad technology scope conflicts with bundled dairy-protein-specific report templates.

Mitigation: Review and revise the white-paper framework and HTML template before using the skill for non-dairy technology domains.

Risk: The workflow depends on external PatSnap/Zhihuiya MCP or API services for data access.

Mitigation: Use a dedicated API key with limited access and require confirmation before retrieval or connectivity self-check calls.

Risk: Generated HTML reports may load remote chart JavaScript.

Mitigation: Prefer bundled or integrity-pinned chart assets before sharing reports in sensitive environments.

Risk: Strategic conclusions can be misleading if upstream patent retrieval, screening, or tagging is incomplete.

Mitigation: Verify that input data has been retrieved, screened, and tagged, and preserve evidence-strength labels for key findings.

## Reference(s):

- [Technology Insight Analysis Skill](https://clawhub.ai/yuanzhian-patsnap/skills/technology-insight-analysis)
- [White Paper Framework](references/white-paper-framework.md)
- [HTML Report Template Specification](references/html-report-template-spec.md)
- [PatSnap Zhihuiya Open Platform](https://open.zhihuiya.com/)
- [PatSnap MCP Server Marketplace](https://open.zhihuiya.com/marketplace/mcp-servers)
- [PatSnap Developer Documentation](https://open.patsnap.com/devportal)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown reports or self-contained HTML reports with ECharts visualizations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are constrained to dimensions supported by retrieved, screened, and tagged patent data; HTML reports may depend on configured PatSnap/Zhihuiya MCP access and chart assets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
