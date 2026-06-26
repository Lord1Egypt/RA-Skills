## Description: <br>
xiaobai-print helps an agent use a local MCP bridge to check printer readiness and capabilities, upload local files, create print jobs, and briefly confirm job status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zwwz22](https://clawhub.ai/user/zwwz22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit local or URL-based documents to a configured printer through a local bridge, following a device-check, capability-check, upload, print, and status-confirmation workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local file uploads can expose sensitive documents to the configured printer or upstream MCP service. <br>
Mitigation: Install only when the printer and upstream MCP service are trusted, and confirm the exact local file path before upload. <br>
Risk: Authenticated proxy calls can submit broad printer actions through the local bridge. <br>
Mitigation: Keep the bridge bound to 127.0.0.1, use a scoped token, and avoid changing MY_MCP_BASE_URL or upstream URLs to untrusted hosts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zwwz22/xiaobai-print) <br>
- [Skill instructions](artifact/skills/xiaobai-print/SKILL.md) <br>
- [Tool schema](artifact/skills/xiaobai-print/schema/tools.json) <br>
- [Repository README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON arguments; tool responses are returned as text or JSON from the local bridge.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and MY_MCP_TOKEN; may upload local files and submit authenticated printer actions through the configured MCP bridge.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
