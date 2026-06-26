## Description: <br>
Stocki is an AI financial analyst for A-shares, HK stocks, US stocks, ETFs, indices, sector analysis, financial metrics, concept themes, real-time market data, and quantitative analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[17817942676](https://clawhub.ai/user/17817942676) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Stocki to ask financial market questions, retrieve real-time quotes and sector context, and submit longer quantitative analysis tasks such as screening or backtesting. It is designed for OpenClaw workflows that call the bundled CLI with a Stocki gateway URL and API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The doctor and update paths can replace the installed Stocki skill, including deleting and recloning the installed directory. <br>
Mitigation: Review the installed scripts before running doctor or update commands, and avoid those paths in sensitive environments unless code replacement is acceptable. <br>
Risk: The skill sends user questions, selected preferences, and any explicitly shared portfolio context to the Stocki gateway. <br>
Mitigation: Share portfolio or private financial details only with explicit consent, and configure STOCKI_API_KEY using normal secret hygiene. <br>
Risk: Real-time financial outputs may be unavailable, rate limited, or unsuitable as standalone financial advice. <br>
Mitigation: Treat Stocki output as analysis support, verify material trading decisions independently, and surface gateway errors or quota limits without fabricating data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/17817942676/stocki) <br>
- [Stocki Gateway](https://api.stocki.com.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text from CLI commands, with downloaded analysis files when quant tasks produce reports or images.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instant mode returns direct answers; quant mode returns task identifiers, status text, file listings, and downloaded result files.] <br>

## Skill Version(s): <br>
0.4.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
