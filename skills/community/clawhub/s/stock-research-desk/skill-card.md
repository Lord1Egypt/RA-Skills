## Description: <br>
Claude Code skill for multi-agent equity research that produces buy-side memos with debate, scenario projection, and bilingual DOCX delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wd041216-bit](https://clawhub.ai/user/wd041216-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, analysts, and developers use this skill to research a stock, screen a sector theme, or maintain a watchlist using a multi-agent equity research workflow. It supports bilingual Chinese and English memo delivery and does not execute trades, manage portfolios, or provide a backtesting engine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a sensitive API key for the research workflow. <br>
Mitigation: Use a dedicated or limited API key where possible and avoid committing .env files. <br>
Risk: The skill can run local commands, maintain watchlist state, and write DOCX reports to the desktop. <br>
Mitigation: Review the referenced package or repository before installing or running it, and inspect generated files before relying on them. <br>
Risk: Generated equity research can be incorrect, incomplete, or unsuitable for a trading decision. <br>
Mitigation: Treat outputs as research support, verify cited sources independently, and do not use the skill for trading execution or portfolio management. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wd041216-bit/stock-research-desk) <br>
- [Project Homepage](https://github.com/wd041216-bit/stock-research-desk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and generated bilingual DOCX reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OLLAMA_API_KEY, python3, and pip; may maintain watchlist state and write DOCX reports to the desktop.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
