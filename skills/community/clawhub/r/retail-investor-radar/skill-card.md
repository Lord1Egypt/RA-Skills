## Description: <br>
Retail Investor Radar generates plain-language A-share stock health reports from public market, fundamentals, valuation, capital-flow, and news data for a ticker, company name, or pinyin abbreviation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tkk0124](https://clawhub.ai/user/tkk0124) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can request an informational A-share stock review by code, Chinese name, fuzzy name, or pinyin abbreviation. The skill fetches public market data and uses DeepSeek to generate a readable report covering quote action, fundamentals, valuation, fund flows, news, and risk prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock queries and compiled public market or news data are sent to DeepSeek for report generation. <br>
Mitigation: Use only inputs intended for processing by the external LLM service, and avoid private portfolio details, account credentials, or trading plans. <br>
Risk: Generated reports can be mistaken for personalized financial advice. <br>
Mitigation: Treat the report as an informational summary, not investment advice, and make investment decisions independently or with qualified advice. <br>
Risk: Generated reports and logs are saved locally by default. <br>
Mitigation: Change config.yaml output settings or delete generated files when local persistence is not desired. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tkk0124/retail-investor-radar) <br>
- [DeepSeek Chat Completions API endpoint](https://api.deepseek.com/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown-style report printed to the console and optionally saved as a local .txt file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DEEPSEEK_API_KEY; default configuration saves generated reports under ./reports and logs under ./logs.] <br>

## Skill Version(s): <br>
1.1.0 (source: artifact/SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
