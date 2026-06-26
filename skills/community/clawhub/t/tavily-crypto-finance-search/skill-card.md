## Description: <br>
Provides Tavily-powered web search and URL extraction optimized for crypto, financial markets, Web3, time-filtered news, and research workflows, with responses oriented to Traditional Chinese. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MuTamamo](https://clawhub.ai/user/MuTamamo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run Tavily searches, fetch recent news, perform deeper research searches, or extract page and whitepaper content for crypto, finance, Web3, and related topics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, extraction URLs, and extracted document requests are sent to Tavily using the user's Tavily API key. <br>
Mitigation: Avoid submitting private internal URLs, secrets, credentials, or confidential documents. <br>
Risk: The skill is designed to present results in Traditional Chinese by default, which may not fit every user workflow. <br>
Mitigation: Override the language behavior or translate the response when another language is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MuTamamo/tavily-crypto-finance-search) <br>
- [Tavily](https://tavily.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown, JSON, or brief text search and extraction results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TAVILY_API_KEY and may include source titles, URLs, snippets, published dates, summaries, extracted content, and failed extraction details.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
