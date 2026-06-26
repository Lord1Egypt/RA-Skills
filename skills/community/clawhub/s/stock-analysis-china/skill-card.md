## Description: <br>
Analyzes China A-share portfolios from screenshots or saved holdings, fetches AKShare market data, calculates technical indicators, and returns structured holding-level suggestions in chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lzwaang](https://clawhub.ai/user/lzwaang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with China A-share portfolios use this skill to extract holdings from screenshots or manual entries, update a local portfolio file, and generate technical-analysis reports with market context and per-stock signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process portfolio screenshots and store holdings locally. <br>
Mitigation: Require explicit confirmation before reading unrelated images, and verify extracted holdings before using the analysis. <br>
Risk: The skill can update or clear saved portfolio data. <br>
Mitigation: Confirm changes with the user before overwriting, removing, or clearing holdings. <br>
Risk: The skill includes setup guidance for installing packages, changing environment variables, creating filesystem links, and restarting OpenClaw. <br>
Mitigation: Review commands before execution and require explicit approval for system-level changes. <br>
Risk: Incorrect extracted holdings or market data may produce misleading portfolio guidance. <br>
Mitigation: Treat reports as reference material, validate holdings and data sources, and avoid presenting outputs as financial advice. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lzwaang/stock-analysis-china) <br>
- [Analysis prompt template](references/analysis_prompt_template.md) <br>
- [AKShare issue tracker](https://github.com/akfamily/akshare/issues) <br>
- [Tesseract simplified Chinese language data](https://github.com/tesseract-ocr/tessdata/raw/main/chi_sim.traineddata) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with inline shell commands and local portfolio JSON updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local holdings data and live market data when dependencies and network access are available.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
