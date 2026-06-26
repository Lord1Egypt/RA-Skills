## Description: <br>
Turns story text into structured shot plans and video-generation assets, then uses MiniMax image/video APIs and ffmpeg to assemble a final story video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yhongm](https://clawhub.ai/user/yhongm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, developers, and media teams use this skill to convert story outlines or scripts into shot JSON, generated images, generated video clips, and a merged final video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Story content, prompts, and generated media requests are sent to MiniMax using the user's API key. <br>
Mitigation: Install only when that data sharing is acceptable, review prompts before execution, and protect MINIMAX_API_KEY as a sensitive credential. <br>
Risk: The skill can attempt package-manager installation of ffmpeg when it is missing. <br>
Mitigation: Review or remove the auto-install path and install ffmpeg through an approved process before running the video merge workflow. <br>
Risk: Configurable MiniMax endpoint variables can direct API-key-backed requests to non-default hosts. <br>
Mitigation: Keep MINIMAX_BASE_URL and MINIMAX_IMAGE_URL pointed only at trusted MiniMax-compatible HTTPS endpoints. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yhongm/story-video-skill) <br>
- [MiniMax API Base URL](https://api.minimaxi.com/v1) <br>
- [MiniMax Image Generation Endpoint](https://api.minimaxi.com/v1/image_generation) <br>
- [Story Structure Reference](references/screenwriting/story-structure.txt) <br>
- [Shot Breakdown Reference](references/screenwriting/shot-breakdown.txt) <br>
- [MiniMax Models Reference](references/minimax-api/models-intro.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell commands, JSON shot plans, and generated media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINIMAX_API_KEY and may write shot JSON, image frames, video clips, storyboard text, and final MP4 output under the skill output directories.] <br>

## Skill Version(s): <br>
1.5.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
