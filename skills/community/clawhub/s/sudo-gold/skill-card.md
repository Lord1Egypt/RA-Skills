## Description: <br>
Uses Tavily Search to gather gold-market prices, news, technical indicators, and fundamental context across international and Chinese gold markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FMouseBoy](https://clawhub.ai/user/FMouseBoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve current gold-market information and produce neutral market summaries that include price, technical, fundamental, and risk sections. Outputs should be treated as informational market context, not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tavily receives gold-market search requests and the skill requires a Tavily API key. <br>
Mitigation: Only install when Tavily use is acceptable, protect the API key, and avoid including private portfolio details in prompts that may trigger external search. <br>
Risk: Gold-market summaries can be mistaken for investment advice. <br>
Mitigation: Present outputs as informational context only, keep interpretations neutral, and preserve the non-investment-advice framing from the artifact. <br>


## Reference(s): <br>
- [Gold Technical Indicators Reference](references/technical-indicators.md) <br>
- [Tavily Search API endpoint](https://api.tavily.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown and console text with source-title lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and TAVILY_API_KEY; Tavily answers are truncated in the bundled analysis script.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence, released 2026-03-11) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
