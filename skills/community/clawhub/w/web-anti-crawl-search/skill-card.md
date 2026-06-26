## Description: <br>
Uses a headless browser to search multiple domestic and international search engines for current web results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlutwuwei](https://clawhub.ai/user/dlutwuwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve current search results, news, finance-related pages, and cross-engine comparisons when static knowledge is insufficient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to external search providers. <br>
Mitigation: Avoid secrets, credentials, regulated data, private customer data, and confidential internal project names in queries. <br>
Risk: Browser automation uses stealth behavior and no-sandbox launch flags. <br>
Mitigation: Run the skill in a constrained environment and review these browser settings for site-policy compliance and containment requirements before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlutwuwei/web-anti-crawl-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON search-result lists with titles, links, snippets, and source labels] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are gathered from selected external search providers through browser automation and may vary by provider availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
