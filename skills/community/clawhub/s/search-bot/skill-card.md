## Description: <br>
Real-time web search. Returns current results, titles, URLs, and an AI-synthesized summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unixlamadev-spec](https://clawhub.ai/user/unixlamadev-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Search Bot to retrieve current web results and AI-synthesized findings for news, research, fact checking, documentation lookup, and other topics that require up-to-date information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and a spend token are sent to external AIProx and downstream search providers. <br>
Mitigation: Install only if you trust AIProx and its downstream providers; avoid secrets, private business data, regulated data, and highly personal searches, and prefer a revocable or limited token when available. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/unixlamadev-spec/search-bot) <br>
- [AIProx Homepage](https://aiprox.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown or JSON-style search results with titles, URLs, descriptions, summaries, key findings, query, and result count.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a task string and optional result count; requires AIPROX_SPEND_TOKEN for paid API access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
