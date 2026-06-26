## Description: <br>
Generate vertical satisfying rust restoration shorts (WeryAI): text-to-video or rusty-object image to grind and polish motion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agents use this skill to turn short rust-restoration briefs or rusty-object images into vertical WeryAI video-generation requests with expanded production prompts. It supports satisfying restoration shorts that show corrosion removal, polishing motion, and a final shine reveal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a WERYAI_API_KEY and submits paid video-generation requests. <br>
Mitigation: Install only when the publisher is trusted, keep the API key out of the skill package, and confirm parameters before running paid generation. <br>
Risk: Local image paths can be read and uploaded to WeryAI when used for image-to-video requests. <br>
Mitigation: Prefer public HTTPS image URLs; use local paths only after confirming the exact file path and obtaining explicit consent for upload. <br>
Risk: Unsupported model parameters can cause failed or rejected WeryAI requests. <br>
Mitigation: Validate model, duration, aspect ratio, audio, and image fields against the bundled WeryAI API reference before submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/rust-restore-video) <br>
- [WeryAI video CLI and JSON reference](resources/WERYAI_VIDEO_API.md) <br>
- [WeryAI video API host](https://api.weryai.com) <br>
- [WeryAI model registry and upload host](https://api-growth-agent.weryai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request bodies and shell commands for the WeryAI video CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WERYAI_API_KEY, Node.js 18+, network access, and paid WeryAI generation credits.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
