## Description: <br>
Fetches realtime TradeAlpha news across Reuters, Bloomberg, Truth Social, research alerts, and domestic news sources via POST /api/v1/news/realtime_news, with filters for source, category, level, and time range. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiuwei2](https://clawhub.ai/user/jiuwei2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve and summarize TradeAlpha realtime news, including Reuters, Bloomberg, Truth Social, domestic, and research-alert sources, from natural-language filtering requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad news prompts can use a local TradeAlphaToken and send authenticated requests to quantaccess.lxaa.top. <br>
Mitigation: Install only when TradeAlpha routing is intended, prefer explicit TradeAlpha wording, restrict token scope where possible, and rotate the token if its exposure is uncertain. <br>
Risk: The skill depends on a third-party news API and local Node.js execution, so unavailable execution tools, missing tokens, rate limits, or service errors can prevent results. <br>
Mitigation: Check Node.js availability, set TradeAlphaToken only in the environment, handle documented API error codes, and avoid retry loops when local script execution is unavailable. <br>
Risk: Realtime news may be delayed and should not be treated as guaranteed complete or immediate. <br>
Mitigation: Preserve source and timestamp fields in responses and communicate the documented 0-5 minute delay when presenting results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiuwei2/tradealpha-open-platformv2) <br>
- [TradeAlpha Open Platform](https://quantaccess.lxaa.top/) <br>
- [TradeAlpha realtime news endpoint](https://quantaccess.lxaa.top/api/v1/news/realtime_news) <br>
- [TradeAlpha interface reference](reference.md) <br>
- [TradeAlpha request and response examples](examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown summary with optional JSON-backed news results and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a TradeAlphaToken environment variable; page_size is limited to 100 and news may be delayed by 0-5 minutes.] <br>

## Skill Version(s): <br>
0.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
