## Description: <br>
sudu-gold helps an agent use Tavily search to retrieve gold-market information and summarize price, technical, fundamental, and risk context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FMouseBoy](https://clawhub.ai/user/FMouseBoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for current gold-market summaries, including prices, technical indicators, fundamentals, and risk notes. It is informational and should not be treated as personalized financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gold-market queries and prompt context are sent to Tavily using the user's API key. <br>
Mitigation: Avoid including private financial details, account information, or sensitive personal context in prompts. <br>
Risk: Generated buy/sell commentary may be mistaken for personalized financial advice. <br>
Mitigation: Treat outputs as general market information and review them against the user's own risk tolerance and qualified advice before acting. <br>


## Reference(s): <br>
- [sudu-gold ClawHub release page](https://clawhub.ai/FMouseBoy/sudu-gold) <br>
- [Gold technical indicators reference](references/technical-indicators.md) <br>
- [Tavily Search API endpoint](https://api.tavily.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and console text with source links when search results are returned] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and TAVILY_API_KEY; Tavily answers are truncated in the bundled script before display.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
