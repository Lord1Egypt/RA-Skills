## Description:

Generates bilingual A-share investment research reports with fundamental analysis, Wu Zhaohui breakout technical analysis, valuation scenarios, risk review, charts, and HTML/PDF deliverables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yjkj999999](https://clawhub.ai/user/yjkj999999)

### License/Terms of Use:

MIT-0

## Use Case:

External investors, analysts, and finance teams can use this skill to draft bilingual A-share company research reports from a stock code, company name, or position details. It guides market and financial data collection, technical and valuation analysis, risk review, chart creation, and HTML/PDF report delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may include personal holding details and may be uploaded or shared through public URLs.

Mitigation: Use local-only delivery by default, require explicit approval before upload or sharing, and redact position data from shareable outputs.

Risk: PDF conversion may run Chrome with sandboxing disabled, which increases exposure when converting untrusted HTML.

Mitigation: Convert only trusted local HTML, isolate the conversion environment, or enable Chrome sandboxing before processing untrusted input.

Risk: Financial analysis can be mistaken for investment advice or rely on stale or conflicting market data.

Mitigation: Require current source labels for precise figures, preserve conflicting values instead of choosing silently, avoid buy/sell/hold ratings, and include a clear disclaimer.

## Reference(s):

- [Report Structure Template](references/report_structure.md)
- [Wu Zhaohui Breakout Point Technical System](references/technical_analysis.md)
- [Valuation Framework](references/valuation_framework.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Bilingual Markdown or HTML report drafts, PNG charts, and PDF-ready output with inline code and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include user-provided position details; generated reports should include source labels, falsification signals, and disclaimers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
