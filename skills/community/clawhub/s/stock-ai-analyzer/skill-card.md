## Description:

Stock AI Analyzer guides agents through China A-share fundamental research, including company growth, valuation posture, financial quality, business structure, market-theme fit, competitive position, governance checks, and optional deep research using public market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinfi-codex](https://clawhub.ai/user/chinfi-codex)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to structure China A-share stock research from public data, separating evidence collection from agent-written investment analysis. Developers can also use its scripts to fetch deterministic datasets, scan thesis candidates, persist tracking fields, and render Markdown reports to HTML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database access and default PostgreSQL credentials may expose stored tracking data or allow unintended writes.

Mitigation: Run in a contained environment, configure unique credentials or use SQLite, and restrict the database role to only the required tracking tables.

Risk: Import paths or shared ancestor directories writable by untrusted users or skills could affect script execution.

Mitigation: Keep the skill and shared directories under trusted ownership and deny write access to untrusted users or other skills.

Risk: Downloaded PDFs and generated HTML reports may contain untrusted content.

Mitigation: Validate downloaded content, use strict rendering checks where practical, and avoid opening generated reports in a sensitive browser context.

Risk: The skill supports financial analysis workflows that can produce incorrect or misleading conclusions if evidence is stale or incomplete.

Mitigation: Require current public data, disclose data gaps and uncertainty, and preserve the skill's boundary that scripts provide evidence rather than investment conclusions.

## Reference(s):

- [Deep Mode Research Workflow](references/deep_mode.md)
- [Qualitative Analysis Framework](references/qualitative_framework.md)
- [Quantitative Analysis Framework](references/quantitative_framework.md)
- [Industry Valuation Method Library](references/industry_valuation_library.md)
- [Growth Success Rate Framework](references/growth_success_rate.md)
- [Living Report Structure Contract](references/living_report.md)
- [Engineering Orchestration and Context Management](references/orchestration.md)
- [ClawHub Skill Page](https://clawhub.ai/chinfi-codex/skills/stock-ai-analyzer)
- [Publisher Profile](https://clawhub.ai/user/chinfi-codex)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis with optional JSON evidence packs, shell commands, and self-contained HTML reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent conclusions are written from evidence; scripts are intended for deterministic data fetching, scanning, tracking, and rendering.]

## Skill Version(s):

2.2.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
