## Description: <br>
Stock Terminal turns AI chat into a read-only financial terminal for market research, using SentiSense data to answer typed commands and natural-language stock questions with synthesized reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thesentitrader](https://clawhub.ai/user/thesentitrader) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and finance-oriented agent builders use this skill to turn chat queries such as open, compare, daily brief, smart-money screens, flow, mood, news, and earnings into read-only, data-grounded market research screens. It is informational and educational only, not investment advice or a trading interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Headline resolution can require fetching article URLs chosen from market-data results. <br>
Mitigation: Allow only public HTTP(S) destinations, block private and internal IP ranges including redirects, cap response size and time, and fall back to URL-slug titles when fetching is unavailable or unsafe. <br>
Risk: Optional social embeds can introduce third-party HTML into the host interface. <br>
Mitigation: Sanitize or sandbox third-party embed HTML, or render native or plain-link cards when sandboxing is not available. <br>
Risk: The skill requires a SentiSense API key for read-only market-data calls. <br>
Mitigation: Store the key only in host environment state and keep it out of prompts, tool arguments, logs, emitted events, and user-facing output. <br>


## Reference(s): <br>
- [Stock Terminal on ClawHub](https://clawhub.ai/thesentitrader/skills/stock-terminal) <br>
- [Publisher Profile](https://clawhub.ai/user/thesentitrader) <br>
- [SentiSense](https://sentisense.ai) <br>
- [SentiSense Skill API Reference](https://sentisense.ai/skill.md) <br>
- [SentiSense App](https://app.sentisense.ai) <br>
- [SentiSense Developer Settings](https://app.sentisense.ai/settings/developer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with terminal-screen templates, JSON-like artifact examples, and inline code or shell blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SentiSense API key for read-only market-data lookups; no trading, purchases, write operations, or wallet access.] <br>

## Skill Version(s): <br>
1.3.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
