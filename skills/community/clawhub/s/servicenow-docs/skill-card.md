## Description: <br>
Search and retrieve ServiceNow documentation, release notes, and developer docs (APIs, references, guides). Uses docs.servicenow.com via Zoomin and developer.servicenow.com APIs for developer topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheSethRose](https://clawhub.ai/user/TheSethRose) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, administrators, and support teams use this skill to find and summarize ServiceNow platform documentation, release notes, developer guides, and API references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner reports that the article-fetch tool can be directed to fetch non-ServiceNow URLs. <br>
Mitigation: Review requested article URLs before use and prefer versions that restrict fetching to expected ServiceNow documentation domains over HTTPS. <br>
Risk: Documentation results may be incomplete or depend on current ServiceNow documentation availability. <br>
Mitigation: Verify important guidance against the linked ServiceNow documentation before applying it in production. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheSethRose/servicenow-docs) <br>
- [ServiceNow product documentation](https://docs.servicenow.com/) <br>
- [ServiceNow Developer documentation](https://developer.servicenow.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with documentation links and summarized results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search and guide outputs may be truncated; some API reference results return links that require browser access for full content.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
