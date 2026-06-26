## Description: <br>
VPick AI Video Creator helps agents guide end-to-end VPick video workflows, including image and video generation, voiceover, music, lip sync, audio processing, clip combining, and export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snoopyrain](https://clawhub.ai/user/snoopyrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, and production teams use this skill to have an agent plan and operate VPick canvas workflows for AI video production, from asset generation through audio and final export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The VPick MCP URL contains an authentication token that can trigger generations and consume credits if exposed. <br>
Mitigation: Treat the MCP URL like a password, monitor VPick credit usage, and regenerate the token if it is exposed. <br>
Risk: Prompts and uploaded media are processed by VPick and routed to third-party model providers. <br>
Mitigation: Install only if you trust VPick and its listed providers with the prompts and media used in generation workflows. <br>
Risk: Large video, image, and audio generations can spend the user's VPick credit balance. <br>
Mitigation: Check credit usage and planned generation scope before running large or repeated production workflows. <br>


## Reference(s): <br>
- [VPick MCP Connection Guide](https://vpick-doc.10xboost.org/guide/mcp-connection.html) <br>
- [VPick App](https://vpick.10xboost.org) <br>
- [ClawHub skill listing](https://clawhub.ai/snoopyrain/vpick-ai-video-creator) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with inline tool-call and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes VPick MCP workflow steps, model choices, credit considerations, and error-handling guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
