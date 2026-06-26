## Description: <br>
Fetches recent category-specific news from ZAKER for technology, finance, sports, entertainment, automotive, domestic, international, military, and internet topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zaker-coder](https://clawhub.ai/user/zaker-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to request focused, current news in a specific category or to drill down from broader headlines into domains such as technology, finance, sports, entertainment, automotive, domestic, international, military, or internet news. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts skills.myzaker.com for news queries and presents links returned by that service. <br>
Mitigation: Install only when this external API contact is acceptable, and review returned links before relying on or sharing them. <br>
Risk: Broad trigger examples may cause the agent to select the skill for ambiguous category or language requests. <br>
Mitigation: Narrow invocation triggers or clarify language preference handling before deployment in tightly controlled workflows. <br>


## Reference(s): <br>
- [ZAKER category article API](https://skills.myzaker.com/api/v1/article/category?v=1.0.6) <br>
- [ClawHub skill page](https://clawhub.ai/zaker-coder/zaker-category-news) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown] <br>
**Output Format:** [Markdown news list with linked article titles, summaries, authors, and publish times] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns up to 20 category articles per request from the documented ZAKER API.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence; artifact frontmatter lists 1.0.7) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
