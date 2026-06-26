## Description: <br>
AIPex Browser provides AI-powered browser automation through the AIPex Chrome Extension and MCP bridge for navigating pages, clicking elements, filling forms, capturing screenshots, managing tabs, and downloading content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buttercannfly](https://clawhub.ai/user/buttercannfly) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation users use this skill to connect an agent to Chrome through the AIPex extension and MCP bridge for browser navigation, form interaction, screenshots, downloads, tab management, and browser-assisted testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad control over Chrome and browser-visible data. <br>
Mitigation: Use a separate Chrome profile or close sensitive tabs before enabling the bridge. <br>
Risk: Browser automation can trigger account actions, purchases, submissions, deletions, downloads, or screenshots. <br>
Mitigation: Require explicit user approval before high-impact browser actions or sending screenshots to the LLM. <br>
Risk: The MCP bridge is launched through npx, which can download code at runtime. <br>
Mitigation: Pin or verify the bridge package where possible before use. <br>


## Reference(s): <br>
- [AIPex homepage](https://aipex.ai) <br>
- [AIPex Browser Tools Reference](references/tools-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Configuration instructions, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18 or newer, npx, the AIPex Chrome extension, and a local MCP bridge connection.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
