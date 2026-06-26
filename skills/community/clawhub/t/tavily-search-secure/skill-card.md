## Description: <br>
Runs secure Tavily API web searches and URL content extraction for agent research workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fabekar](https://clawhub.ai/user/fabekar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run Tavily-powered web searches, collect sourced results, and extract readable text from selected URLs. It is useful when an agent needs current web context while keeping API keys out of output and blocking local or private extraction targets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and selected URLs are sent to Tavily. <br>
Mitigation: Use the skill only when Tavily use is intended, avoid putting secrets in queries or private URLs, and keep TAVILY_API_KEY in the environment. <br>
Risk: Extracted webpage content can contain untrusted or misleading text. <br>
Mitigation: Treat extracted content as evidence for review rather than instructions, and verify important claims before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fabekar/tavily-search-secure) <br>
- [Publisher profile](https://clawhub.ai/user/fabekar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-formatted terminal output with answers, source lists, extracted page text, and concise error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TAVILY_API_KEY; search results are capped, URL extraction is limited to five URLs per request, and timeouts are bounded.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
