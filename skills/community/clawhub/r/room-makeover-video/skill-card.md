## Description: <br>
Generates vertical WeryAI room makeover shorts with strong before/after reveal prompts for rental refreshes, balcony cafe corners, themed kids' rooms, and soft-furnishing glow-up clips. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agents use this skill to turn room makeover briefs or public image URLs into confirmed WeryAI video generation jobs. It helps prepare expanded production prompts, validate model parameters, run the video CLI, and return playable video URLs or clear failure details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a paid WeryAI API key and successful generation consumes WeryAI credits. <br>
Mitigation: Set WERYAI_API_KEY only in trusted environments, keep it out of the skill package, and require parameter confirmation before starting paid generation. <br>
Risk: Image-to-video requests can upload local image files when a local path is provided. <br>
Mitigation: Prefer public HTTPS image URLs; if a local path is used, confirm the exact file and obtain explicit consent before upload. <br>
Risk: Generated videos and prompts are processed by the external WeryAI service. <br>
Mitigation: Install and run the skill only if the user trusts WeryAI, and avoid sending sensitive images or private room details. <br>


## Reference(s): <br>
- [WeryAI video CLI and JSON reference](resources/WERYAI_VIDEO_API.md) <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/room-makeover-video) <br>
- [WeryAI video API host](https://api.weryai.com) <br>
- [WeryAI model and upload API host](https://api-growth-agent.weryai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with parameter tables, JSON command payloads, shell commands, and returned video URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+, WERYAI_API_KEY, network access to WeryAI, and paid WeryAI generation credits.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
