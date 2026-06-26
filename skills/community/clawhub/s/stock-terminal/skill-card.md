## Description: <br>
Stock Terminal helps agents answer stock and market research questions with read-only SentiSense data, terminal-style reports, and concise financial context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thesentitrader](https://clawhub.ai/user/thesentitrader) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to provide external users with stock screens, market briefs, comparisons, sentiment views, smart-money flow, news, stories, and earnings calendars. Outputs are informational and educational, not investment advice or trade execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a SentiSense API key for read-only financial data. <br>
Mitigation: Store the key as a host secret, send it only in authenticated API headers, and never include it in user-facing output. <br>
Risk: Optional headline fetching and social embeds may retrieve or render untrusted public web content. <br>
Mitigation: Restrict outbound fetching to safe public URLs, cap response size and redirects, and sanitize oEmbed HTML before display. <br>
Risk: Financial reports may be mistaken for personalized recommendations. <br>
Mitigation: Keep output framed as informational education and avoid instructions to buy, sell, or trade securities. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thesentitrader/skills/stock-terminal) <br>
- [SentiSense Website](https://sentisense.ai) <br>
- [SentiSense API Reference](https://sentisense.ai/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown terminal-style reports, concise prose, and occasional bash examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SENTISENSE_API_KEY for read-only data access; responses should avoid exposing API keys and avoid personalized investment recommendations.] <br>

## Skill Version(s): <br>
1.2.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
