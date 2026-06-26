## Description: <br>
Intelligent RSS subscription and summarization for subscribing to, fetching, filtering, and summarizing RSS or Atom feeds when users need to track news and blog updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanan9812](https://clawhub.ai/user/wanan9812) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage RSS or Atom subscriptions, fetch recent feed items, filter them by configured keywords, and return concise feed summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feed URLs and preferences are stored in local data files. <br>
Mitigation: Avoid adding sensitive private feeds unless local storage of those URLs and preferences is acceptable. <br>
Risk: Fetched feed titles, links, publication dates, and snippets may be returned to the agent for summarization. <br>
Mitigation: Use public or approved feeds, and review configured subscriptions before fetching when confidential feed contents are possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wanan9812/rss-summarizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, configuration] <br>
**Output Format:** [JSON script responses containing RSS feed items, errors, configuration results, or markdown/plain-text summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores subscription URLs and preferences in local JSON data files; fetched feed titles, links, dates, and snippets may be returned to the agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
