## Description: <br>
Web search via Tavily API with built-in monthly usage tracking and quota management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neverland83](https://clawhub.ai/user/neverland83) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Tavily web searches, return sourced results in Markdown or JSON, and keep monthly usage within a configured quota. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Tavily using the configured TAVILY_API_KEY. <br>
Mitigation: Use only for queries appropriate to send to Tavily, keep the API key secret, and follow the account's Tavily terms and access controls. <br>
Risk: The local monthly usage counter may not match Tavily account usage if searches run with --no-count or outside this skill. <br>
Mitigation: Monitor Tavily account usage directly and keep the configured monthly limit below the account quota. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/neverland83/tavily-metered-search) <br>
- [Tavily](https://tavily.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown search results or JSON search result objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include a Tavily short answer and local quota warning; result count is clamped to 1-10.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
