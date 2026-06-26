## Description: <br>
Use a local DDGS MCP server via mcporter to access web, news, image, video, and book search tools without API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[firefrog-pepe](https://clawhub.ai/user/firefrog-pepe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run general web, news, image, video, and book searches through a local DDGS MCP server exposed via mcporter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on running a local DDGS search service and connecting mcporter to it. <br>
Mitigation: Keep the service bound to localhost and verify the DDGS server and mcporter configuration before use. <br>
Risk: Search queries may contain sensitive information and are sent to external search backends through DDGS. <br>
Mitigation: Avoid sensitive searches and use explicit backend, region, safesearch, and result-limit settings when reproducibility or filtering matters. <br>
Risk: The optional systemd service can keep the search server running across sessions. <br>
Mitigation: Enable the persistent service only when intentionally needed, and disable or stop it when the local endpoint should not remain available. <br>


## Reference(s): <br>
- [Local DDGS API docs](http://localhost:8000/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash command examples and JSON tool-call output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local mcporter calls to DDGS MCP tools for text, news, images, videos, and books search.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
