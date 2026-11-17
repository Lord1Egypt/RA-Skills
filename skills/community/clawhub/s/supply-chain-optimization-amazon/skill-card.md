## Description:

Supply Chain Optimization (Lite) - Diagnose bottlenecks and provide cost reduction strategies through conversation

This skill is ready for commercial/non-commercial use.

## Publisher:

[phheng](https://clawhub.ai/user/phheng)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers use this skill to diagnose supply chain bottlenecks, review margin and inventory metrics, and receive cost reduction recommendations through a guided conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports load unpinned third-party Chart.js from a CDN, which can access the report's business data when opened.

Mitigation: Prefer text or Markdown reports for sensitive data, or bundle and pin Chart.js with integrity checks before using the HTML report workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phheng/skills/supply-chain-optimization-amazon)
- [Nexscope AI](https://www.nexscope.ai/)
- [Chart.js CDN dependency](https://cdn.jsdelivr.net/npm/chart.js)

## Skill Output:

**Output Type(s):** [text, markdown, HTML, shell commands, guidance]

**Output Format:** [Markdown-style diagnostic reports with tables, optional generated Markdown or HTML report files, and inline bash commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configurable benchmark thresholds for margin, shipping cost, inventory days, cash cycle, and net margin.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
