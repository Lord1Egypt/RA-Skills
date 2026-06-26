## Description: <br>
Search Reddit in real time using OpenAI web_search with enrichment for engagement metrics and top comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arkaydeus](https://clawhub.ai/user/arkaydeus) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to find recent Reddit threads, filter searches by subreddit or date range, and collect enriched thread context such as score, comment count, and top comment excerpts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to OpenAI and public Reddit endpoints. <br>
Mitigation: Use a dedicated OpenAI API key where possible and monitor usage costs. <br>
Risk: Returned Reddit content is untrusted public web text. <br>
Mitigation: Review results before relying on them or passing them into downstream workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arkaydeus/search-reddit) <br>
- [Artifact README](README.md) <br>
- [OpenAI Platform](https://platform.openai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, links] <br>
**Output Format:** [Markdown search results, compact text, links-only text, or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may include Reddit thread URLs, subreddit names, dates, engagement metrics, and top comment excerpts.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
