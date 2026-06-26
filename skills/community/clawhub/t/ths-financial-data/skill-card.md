## Description: <br>
This skill helps agents retrieve stock market data, resolve Chinese names and abbreviations into thsdk stock codes, and format real-time quotes, fund flow, K-line, and Wencai query results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bensema](https://clawhub.ai/user/bensema) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to look up securities, fetch market data, and prepare stock-analysis outputs for A-share, Hong Kong, and U.S. market workflows. It is useful when an assistant needs to turn natural-language or abbreviated stock inputs into structured market data and user-facing Markdown tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically install or upgrade the thsdk Python package during normal use. <br>
Mitigation: Run it in an isolated Python environment and preinstall a reviewed, pinned thsdk version before use. <br>
Risk: THS credentials may be needed for the data provider. <br>
Mitigation: Provide credentials only in the execution environment where they are required, and avoid placing them in prompts, skill files, or generated outputs. <br>
Risk: Real-time market data may be delayed or unavailable depending on the upstream provider and account permissions. <br>
Mitigation: Treat returned prices and analysis as informational, verify important market data against an authoritative source, and surface provider errors to the user. <br>


## Reference(s): <br>
- [thsdk API Reference](references/api_reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/bensema/ths-financial-data) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables, Python snippets, structured Python dictionaries, and pandas DataFrames] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May prompt for user selection when a symbol search returns multiple matching securities.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
