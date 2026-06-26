## Description: <br>
Stock Ai Analyzer helps agents perform structured fundamental research on China A-share companies, including data collection, valuation framing, governance review, announcement checks, and optional deep-dive investigation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinfi-codex](https://clawhub.ai/user/chinfi-codex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to analyze China A-share stocks from public financial, market, filing, announcement, and governance data. The skill supports concise research reports as well as deeper investigations that separate source facts from model judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce financial research that may be mistaken for investment advice. <br>
Mitigation: Treat outputs as research support, verify conclusions against current public filings and market data, and make independent investment decisions. <br>
Risk: The skill requires a Tushare token and may fetch public data, cache results locally, and write evidence files. <br>
Mitigation: Provide only the intended Tushare credential, review generated files before sharing them, and avoid including sensitive personal or account data in prompts or outputs. <br>
Risk: Public filings, announcements, and extracted PDF text can be incomplete, stale, or misread by an agent. <br>
Mitigation: Use the skill's source-fact versus model-judgment discipline, read primary announcement or report text for material claims, and lower confidence when data is missing. <br>


## Reference(s): <br>
- [Stock Ai Analyzer ClawHub page](https://clawhub.ai/chinfi-codex/stock-ai-analyzer) <br>
- [qualitative_framework.md](references/qualitative_framework.md) <br>
- [quantitative_framework.md](references/quantitative_framework.md) <br>
- [industry_valuation_library.md](references/industry_valuation_library.md) <br>
- [growth_success_rate.md](references/growth_success_rate.md) <br>
- [deep_mode.md](references/deep_mode.md) <br>
- [orchestration.md](references/orchestration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON evidence and context files, optional HTML reports, and shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local evidence packs, module context JSON, cached public data, downloaded filings, and self-contained HTML reports when requested.] <br>

## Skill Version(s): <br>
2.2.5 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
