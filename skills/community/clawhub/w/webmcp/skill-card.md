## Description:

This skill should be used when browsing or automating web pages that expose tools via the WebMCP API (window.navigator.modelContext). It teaches agents how to discover, inspect, and invoke WebMCP tools on websites instead of relying on DOM scraping or UI actuation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brunobuddy](https://clawhub.ai/user/brunobuddy)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to identify websites that expose WebMCP tools, inspect their JSON Schema inputs, invoke suitable page-provided tools, and fall back to DOM interaction when no suitable tool is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Website-provided tools may perform sensitive actions such as purchases or account changes.

Mitigation: Require browser prompts and explicit user confirmation before executing sensitive tool calls, and respect user denials without retrying cancelled calls.

Risk: Page tools are dynamic and may change after navigation or single-page application state updates.

Mitigation: Re-discover available tools after page transitions or state changes before choosing and invoking a tool.

Risk: A tool call may fail or be inappropriate if parameters do not match the exposed JSON Schema.

Mitigation: Inspect each tool's input schema and invoke tools only with parameters that match required fields and declared types.

## Reference(s):

- [WebMCP specification](https://github.com/webmachinelearning/webmcp)
- [ClawHub skill page](https://clawhub.ai/brunobuddy/skills/webmcp)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JavaScript examples and structured tool-call recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the tools exposed by the active browser page and may require explicit user confirmation for sensitive actions.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
