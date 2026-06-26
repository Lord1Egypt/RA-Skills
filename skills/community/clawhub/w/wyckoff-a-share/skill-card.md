## Description: <br>
Run Wyckoff-style A-share analysis from stock codes, holdings, cash, CSV data, and optional chart images with online source fallback and Beijing-time trading-session checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YoungCan-Wang](https://clawhub.ai/user/YoungCan-Wang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to analyze A-share symbols, portfolios, cash deployment, or uploaded market files through a Wyckoff workflow. The skill produces session-aware market analysis, data audit details, portfolio action guidance, and charting code or chart output when plotting is allowed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can generate buy, sell, rotation, or cash-deployment suggestions for A-share portfolios. <br>
Mitigation: Treat outputs as informational financial analysis only, not trading authorization or personalized financial advice. <br>
Risk: Portfolio holdings, costs, quantities, and cash balances may be sensitive. <br>
Mitigation: Avoid sharing portfolio details unless the user accepts that they will be processed for the requested analysis. <br>
Risk: The skill may provide Python charting code or commands. <br>
Mitigation: Review generated code before running it and execute it only in a sandboxed environment. <br>
Risk: Online market lookups may expose stock symbols and event dates to public financial data sources. <br>
Mitigation: Use the skill only when public-source A-share lookup is acceptable for the requested symbols and dates. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/YoungCan-Wang/wyckoff-a-share) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Source fallback policy](artifact/rules/source-fallbacks.md) <br>
- [Analysis and plotting prompt](artifact/rules/alpha-system-prompt.md) <br>
- [OpenAI agent configuration](artifact/agents/openai.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with structured sections and optional Python plotting code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include data audit tables, session verdicts, Wyckoff event labels, portfolio action labels, and chart generation instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
