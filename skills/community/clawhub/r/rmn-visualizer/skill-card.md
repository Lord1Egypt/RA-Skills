## Description: <br>
Visualizes local AI agent memory files as an interactive five-layer recursive memory network using a Node.js server and D3.js force-directed graph. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weidadong2359](https://clawhub.ai/user/weidadong2359) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to inspect local agent memory files, memory folders, and issue notes as a visual network for debugging, review, and memory exploration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The launch path can expose local agent memory and issue-file contents through an unauthenticated public Cloudflare URL. <br>
Mitigation: Prefer local-only mode with serve.js, review memory files before launch, and avoid launch.js or URL sharing when the workspace may contain secrets, customer data, private notes, prompts, credentials, or account details. <br>
Risk: The skill reads local memory-related files from the selected workspace. <br>
Mitigation: Set RMN_WORKSPACE only to a workspace intended for visualization and remove sensitive files before running the server. <br>


## Reference(s): <br>
- [RMN Visualizer ClawHub Release](https://clawhub.ai/weidadong2359/rmn-visualizer) <br>
- [Publisher Profile](https://clawhub.ai/user/weidadong2359) <br>
- [Cloudflare Tunnel Downloads](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown text with inline shell commands and service URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return a local service URL or a Cloudflare Tunnel URL for the visualization.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
