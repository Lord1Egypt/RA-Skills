## Description: <br>
Comprehensive research grounded in web data with explicit citations for multi-source synthesis, comparisons, current events, market analysis, and detailed reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evanYDL](https://clawhub.ai/user/evanYDL) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other external users can use this skill to run Tavily-backed web research from an agent workflow, choosing a quick or deeper model and optionally saving results to a file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research prompts are sent to Tavily. <br>
Mitigation: Avoid including secrets, private data, or sensitive internal context in research queries. <br>
Risk: The skill can reuse a Tavily token from the local MCP auth cache. <br>
Mitigation: Prefer setting TAVILY_API_KEY explicitly when possible and review the local auth cache behavior before deployment. <br>
Risk: The automatic OAuth path can fetch and run an npm helper during authentication. <br>
Mitigation: Review the OAuth flow and npm helper usage before relying on automatic authentication in managed environments. <br>


## Reference(s): <br>
- [ClawHub Tavily Research skill](https://clawhub.ai/evanYDL/tavily-research) <br>
- [Tavily](https://tavily.com) <br>
- [Tavily MCP endpoint](https://mcp.tavily.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain text research results with citations; optional file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a required research topic, an optional model selection of mini, pro, or auto, and an optional output file path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
