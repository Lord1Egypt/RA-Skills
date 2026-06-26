## Description: <br>
Design, preview, and generate UI code using Google Stitch (via MCP). Helps developers choose the best UI by generating previews first, allowing iteration, and then exporting code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a2mus](https://clawhub.ai/user/a2mus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and designers use this skill to generate UI concepts from text, review preview images, iterate on feedback, and export HTML/CSS after approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup can persistently add a Stitch MCP server that runs the external npm package stitch-mcp-auto through npx. <br>
Mitigation: Review the package before installing, prefer pinning or independently verifying it, and confirm the mcporter configuration change before applying it. <br>
Risk: The workflow may require Google Cloud authentication and project access. <br>
Mitigation: Use a dedicated least-privileged Google Cloud account or project and manually confirm authentication, project creation, and file write actions. <br>
Risk: Generated UI code may not match project requirements or may be produced before the design is approved. <br>
Mitigation: Review preview images first, iterate on feedback, and fetch or save HTML/CSS only after explicit user approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/a2mus/stitch-ui-designer) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, images] <br>
**Output Format:** [Markdown guidance with inline shell commands, MCP tool calls, preview images, and generated HTML/CSS code.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npx and mcporter; generated code is fetched only after user approval of a preview.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
