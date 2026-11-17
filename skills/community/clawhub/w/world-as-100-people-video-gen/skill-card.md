## Description:

Creates short vertical WeryAI videos using a world-as-100-people metaphor with timed English captions, stat-themed icon motion, and a final punchline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, educators, marketers, and developers use this skill to turn demographic themes or chart image URLs into a confirmed WeryAI prompt and CLI request for short vertical infographic videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and deliberately provided image inputs are sent to WeryAI during generation.

Mitigation: Install and run only when users are comfortable sharing those prompts and selected images with WeryAI.

Risk: Local image paths can be read and uploaded to WeryAI if passed as image inputs.

Mitigation: Prefer public HTTPS image URLs; verify any local path and obtain explicit consent before allowing local file upload.

Risk: The skill can make paid WeryAI API requests using WERYAI_API_KEY.

Mitigation: Use a scoped or short-lived environment, keep the API key secret, and confirm generation parameters before executing paid submit or wait commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/world-as-100-people-video-gen)
- [Publisher profile](https://clawhub.ai/user/zoucdr)
- [WeryAI video CLI and JSON reference](resources/WERYAI_VIDEO_API.md)
- [WeryAI video API host](https://api.weryai.com)
- [WeryAI model and upload API host](https://api-growth-agent.weryai.com)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON CLI parameters, shell commands, and playable video links or error details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WERYAI_API_KEY and Node.js 18+; uses paid network calls to WeryAI; normal image inputs should be public HTTPS URLs.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
