## Description: <br>
Provides a six-dimension A-share stock analysis framework and command-line tools for stock analysis, portfolio monitoring, and briefing generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clementgu](https://clawhub.ai/user/clementgu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to structure A-share stock reviews, inspect technical and fundamental signals, monitor holdings, and generate portfolio briefings. Outputs are informational and should be checked against authoritative market and financial sources before use in investment decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the monitor or briefing scripts may read a local holdings file and disclose portfolio-derived stock symbols to Sina Finance during quote lookups. <br>
Mitigation: Review before installation if portfolio data is sensitive; avoid those scripts, remove the local holdings file, or edit the scripts to prevent ticker-level disclosure. <br>
Risk: Stock reports and trading signals may be incomplete, stale, or unsuitable as investment advice. <br>
Mitigation: Treat generated analysis as informational and validate it against authoritative financial disclosures, market data, and professional judgment before making investment decisions. <br>


## Reference(s): <br>
- [Fundamental Analysis Guide](references/fundamental.md) <br>
- [Technical Analysis Guide](references/technical.md) <br>
- [Sina Finance](https://finance.sina.com.cn) <br>
- [ClawHub Skill Page](https://clawhub.ai/clementgu/stock-analysis-framework) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance and terminal text reports from Python scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured analysis reports, monitoring summaries, and portfolio briefings; some scripts perform live quote lookups.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
