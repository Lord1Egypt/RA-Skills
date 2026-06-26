## Description: <br>
This skill should be used when browsing or automating web pages that expose tools via the WebMCP API (window.navigator.modelContext). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brunobuddy](https://clawhub.ai/user/brunobuddy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to discover, inspect, and invoke structured tools exposed by websites through WebMCP instead of relying only on DOM scraping or UI actuation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Website-provided tools may perform sensitive actions such as purchases, account changes, posting, or deleting content. <br>
Mitigation: Use the skill on trusted sites and keep explicit user confirmation for sensitive operations. <br>
Risk: WebMCP tools are dynamic, page-scoped, and permission-gated, so available tools can change after navigation or SPA state updates. <br>
Mitigation: Re-discover available tools after page transitions and invoke only tools whose name, description, and JSON Schema match the user's goal. <br>


## Reference(s): <br>
- [WebMCP specification](https://github.com/webmachinelearning/webmcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, API Calls] <br>
**Output Format:** [Markdown with inline JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses JSON Schema parameters exposed by each website; requires a live browser context.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
