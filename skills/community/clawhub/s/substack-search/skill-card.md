## Description: <br>
Scrape AI-related articles from Substack search with browser automation, extracting titles, authors, summaries, and recent-result context into a numbered digest. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goog](https://clawhub.ai/user/goog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill when they need an agent to search Substack for recent posts or news on a topic and return the findings as a concise digest. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill opens Substack search pages through browser automation, which may use existing browser state. <br>
Mitigation: Use a clean browser profile when existing Substack login state should not be involved. <br>
Risk: Search extraction depends on the current Substack page structure and may produce formatting or argument-handling issues. <br>
Mitigation: Review returned results for formatting and completeness before relying on the digest. <br>


## Reference(s): <br>
- [Browser Automation Flow](references/browser-flow.md) <br>
- [Substack Search Page](https://substack.com/search/QUERY?utm_source=global-search&searching=all_posts&dateRange=day) <br>
- [ClawHub Skill Page](https://clawhub.ai/goog/substack-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown numbered digest with optional JSON from the extraction script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses browser automation and may reflect the current Substack page state and available search results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
