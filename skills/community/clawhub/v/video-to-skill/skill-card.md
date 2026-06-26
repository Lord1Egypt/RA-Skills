## Description: <br>
Generates an OpenClaw Skill from online video content by extracting subtitles or audio, summarizing the content, creating a SKILL.md file, and optionally publishing it to GitHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eeyan2025-art](https://clawhub.ai/user/eeyan2025-art) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to turn public video links into reusable OpenClaw skills. It supports workflows that need transcript extraction, video summarization, SKILL.md generation, and optional repository publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video content may be sent to MiniMax APIs during transcription and summarization. <br>
Mitigation: Use only public, non-confidential videos and review applicable service and data-handling requirements before execution. <br>
Risk: Generated skills can be pushed to GitHub without a strong built-in review gate. <br>
Mitigation: Use a fine-grained GitHub token limited to the intended repository and inspect the generated SKILL.md plus git diff before publishing. <br>
Risk: The audio fallback may install yt-dlp automatically when it is missing. <br>
Mitigation: Run in an isolated environment or preinstall approved, pinned dependencies before using the fallback path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eeyan2025-art/video-to-skill) <br>
- [Publisher profile](https://clawhub.ai/user/eeyan2025-art) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Generated SKILL.md Markdown file, local file paths, shell command output, and optional GitHub link.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a video URL and may require MINIMAX_API_KEY and GITHUB_TOKEN for API processing and publishing.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
