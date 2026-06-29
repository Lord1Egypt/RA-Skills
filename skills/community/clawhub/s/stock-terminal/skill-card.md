## Description: <br>
Stock terminal for AI agents. Turns chat into a futuristic financial terminal: typed commands like "open NVDA", "screen smart-money", "daily brief", or natural questions like "what's hot today?" return composite synthesized reports across price, sentiment, insider trades, congressional disclosures, institutional flows, analyst ratings, AI insights, and embedded news. Read-only. No trading, no purchases, no write operations, no wallet access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thesentitrader](https://clawhub.ai/user/thesentitrader) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn stock and market-research prompts into dense, read-only terminal-style reports grounded in SentiSense market data. It supports ticker lookups, comparisons, daily briefs, market mood, smart-money flow, earnings calendars, and sentiment-tagged news without trading or wallet actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a SentiSense API key and makes network requests for market data. <br>
Mitigation: Install only when API-key use and read-only market-data requests are acceptable; store the key in the host environment and avoid exposing it in user-facing output. <br>
Risk: Third-party news embeds and arbitrary source URLs may introduce privacy, content, or rendering risks. <br>
Mitigation: Sandbox or sanitize third-party embeds, limit arbitrary URL fetching, and degrade to plain links or source labels when title or embed retrieval is unavailable. <br>
Risk: Vague prompts such as "what's the news" can trigger broad market-data retrieval without clear intent. <br>
Mitigation: Ask for clarification when market intent or ticker context is unclear. <br>


## Reference(s): <br>
- [Stock Terminal on ClawHub](https://clawhub.ai/thesentitrader/skills/stock-terminal) <br>
- [SentiSense Website](https://sentisense.ai) <br>
- [SentiSense API Reference](https://sentisense.ai/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, shell commands, guidance] <br>
**Output Format:** [Markdown or structured terminal-style text with occasional inline bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SENTISENSE_API_KEY for authenticated read-only market-data requests.] <br>

## Skill Version(s): <br>
1.2.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
