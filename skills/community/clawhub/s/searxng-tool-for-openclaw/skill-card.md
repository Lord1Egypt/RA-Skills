## Description: <br>
Install an OpenClaw plugin that adds SearXNG-powered web search without paid search APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[barrontang](https://clawhub.ai/user/barrontang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and configure a SearXNG-backed search tool for agent workflows without paid search APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and returned result text pass through the configured SearXNG instance. <br>
Mitigation: Use a SearXNG instance you control or trust, and avoid submitting secrets or sensitive data in search queries. <br>
Risk: Web results returned by SearXNG can contain untrusted or misleading content. <br>
Mitigation: Treat returned pages and snippets as untrusted input and verify important information before acting on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/barrontang/searxng-tool-for-openclaw) <br>
- [Repository](https://github.com/barrontang/searxng-tool-for-openclaw) <br>
- [Documentation](https://github.com/barrontang/searxng-tool-for-openclaw#readme) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, configuration, guidance] <br>
**Output Format:** [Structured JSON search results with setup guidance in Markdown and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search result count is configurable; default maximum is 8 results and supported range is 1 to 50.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
