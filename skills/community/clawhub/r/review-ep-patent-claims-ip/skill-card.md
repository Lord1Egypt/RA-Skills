## Description:

Reviews European patent application claims and supporting application materials for EPO/EPC examination readiness, including clarity, support, sufficiency, added-matter, unity, novelty, inventive-step positioning, claim interpretation, amendment options, fallback positions, and European patent attorney-style drafting quality control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External patent practitioners, drafting teams, and patent-focused agents use this skill to review European patent claim sets and supporting materials for EPC examination readiness, EPO-practice risks, and amendment options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outputs may be mistaken for legal advice or a final patentability opinion.

Mitigation: Treat outputs as practitioner-style drafting analysis and have qualified counsel review them before relying on prosecution, validity, or filing decisions.

Risk: Novelty, inventive-step, family, status, or prior-art conclusions may be incomplete if external patent retrieval was not executed.

Mitigation: Record whether PatSnap MCP retrieval ran, keep document-only conclusions provisional, and avoid claiming a prior-art search unless the tool execution and search strategy are reported.

Risk: Confidential patent materials or API credentials could be exposed through prompts, reports, screenshots, or source files.

Mitigation: Use this skill only in an approved environment for confidential materials and avoid putting API keys or sensitive data into prompts or generated reports.

Risk: Connector URLs and MCP service mappings may change over time.

Mitigation: Re-copy current connection URLs from the official PatSnap MCP marketplace before enabling external retrieval.

## Reference(s):

- [2026 EPO Guidelines for Examination](https://www.epo.org/en/legal/guidelines-epc/2026/index.html)
- [G 1/24, Official Journal 2025 A60](https://www.epo.org/en/legal/official-journal/2025/09/a60)
- [2026 Guidelines, F-IV 4.1: Clarity](https://www.epo.org/en/legal/guidelines-epc/2026/f_iv_4_1.html)
- [2026 Guidelines, F-IV 4.2: Claim Interpretation](https://www.epo.org/en/legal/guidelines-epc/2026/f_iv_4_2.html)
- [2026 Guidelines, F-V: Unity](https://www.epo.org/en/legal/guidelines-epc/2026/f_v.html)
- [PatSnap Open Platform](https://open.patsnap.com/)
- [PatSnap Authentication Guide](https://open.patsnap.com/devportal/guides/authentication)
- [PatSnap MCP Marketplace](https://open.patsnap.com/marketplace/mcp-servers)
- [Advanced Patent Search MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [Patent Briefing MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)

## Skill Output:

**Output Type(s):** [analysis, markdown, guidance, configuration]

**Output Format:** [Markdown reports with issue tables, amendment-basis charts, prioritized recommendations, assumptions, and optional MCP setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output is English unless the user requests another language; novelty and inventive-step comments are labeled provisional when no external search was executed.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
