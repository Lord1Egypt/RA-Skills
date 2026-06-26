## Description: <br>
AI-optimized web search via the Tavily API that returns concise, relevant results for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zenghuwei](https://clawhub.ai/user/zenghuwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let agents run Tavily web searches, retrieve concise source-backed results, and extract readable content from requested URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, requested URLs, and API usage are sent to Tavily. <br>
Mitigation: Avoid using the skill for private, regulated, or confidential queries unless sharing that data with Tavily is acceptable. <br>
Risk: URL extraction may expose internal or sensitive page content to Tavily. <br>
Mitigation: Do not submit private internal URLs or sensitive documents for extraction. <br>
Risk: Returned web page text can contain untrusted or misleading content. <br>
Mitigation: Treat search and extraction results as research material, not as executable instructions for the agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zenghuwei/tavily-search-local) <br>
- [Tavily](https://tavily.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown] <br>
**Output Format:** [Markdown-formatted CLI output with answers, source lists, or extracted page content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search result count is clamped from 1 to 20; extracted URL content and failed URL reports are printed as text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
