## Description: <br>
Generates comprehensive company valuation reports as polished HTML/PDF using market data, qualitative research, charts, and valuation frameworks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xliucs](https://clawhub.ai/user/xliucs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and analysts use this skill to generate deep-dive stock valuation reports for a public company ticker, including quantitative data collection, qualitative research synthesis, valuation scenarios, and deliverable HTML/PDF reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated Buy/Sell labels, price targets, technical signals, and options sentiment may be mistaken for financial advice. <br>
Mitigation: Treat outputs as informational analysis only and review conclusions before making investment decisions. <br>
Risk: The workflow may prompt for or receive portfolio details or personal financial information. <br>
Mitigation: Do not provide personal financial information, user-identifiable information, or portfolio position data when using the skill. <br>
Risk: The skill creates local data, cache, chart, HTML, and PDF files under /tmp. <br>
Mitigation: Review and clean generated local files when reports are no longer needed, especially on shared systems. <br>
Risk: The skill uses unpinned third-party Python dependencies and public web or market data sources. <br>
Mitigation: Run in a controlled environment and review dependency versions and source reliability before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xliucs/stock-valuation) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/xliucs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files, analysis] <br>
**Output Format:** [HTML/PDF valuation report with supporting JSON data, embedded charts, and agent-facing command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local report and cache files under /tmp; chart images are embedded as base64 in generated HTML.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
