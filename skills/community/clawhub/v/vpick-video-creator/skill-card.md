## Description: <br>
All-in-one AI video production studio on a visual canvas for generating videos, images, voiceover, music, lip sync, vocal separation, voice changes, and combined exports through VPick. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snoopyrain](https://clawhub.ai/user/snoopyrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to plan, generate, assemble, and export AI video projects through VPick's visual canvas. It helps agents coordinate video, image, audio, lip-sync, voice, and combining workflows while accounting for remote processing and credit usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and uploaded media are processed by VPick and routed to third-party model providers. <br>
Mitigation: Avoid uploading sensitive or rights-restricted media unless VPick and its providers may process and store it. <br>
Risk: The MCP URL contains an embedded authentication token. <br>
Mitigation: Treat the MCP URL as a password and avoid sharing it in chat, logs, or public configuration. <br>
Risk: Generation jobs may spend VPick credits. <br>
Mitigation: Confirm the model, duration, output count, and approximate credit cost before running generation jobs. <br>


## Reference(s): <br>
- [VPick MCP connection guide](https://vpick-doc.10xboost.org/guide/mcp-connection.html) <br>
- [VPick app](https://vpick.10xboost.org) <br>
- [ClawHub skill page](https://clawhub.ai/snoopyrain/vpick-video-creator) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Configuration] <br>
**Output Format:** [Markdown guidance with MCP tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create remote video, image, audio, and project assets through VPick MCP tools.] <br>

## Skill Version(s): <br>
1.0.2 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
