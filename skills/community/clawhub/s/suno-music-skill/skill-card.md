## Description: <br>
AI music generation via Suno API. Submit prompts, style tags, and lyrics to generate songs. Check generation status and download audio/cover art. Use when user asks to create music, generate songs, compose tracks, or produce audio content with AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kennedydqz-del](https://clawhub.ai/user/kennedydqz-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to submit music prompts, lyrics, and style settings to a Suno-compatible API, then check task status and retrieve generated audio or cover-art links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Suno API key and sends prompts, lyrics, task data, and generated-content requests to a remote Suno-compatible service. <br>
Mitigation: Install only when that data sharing is acceptable, and provide the API key through the expected SUNO_API_KEY environment variable rather than embedding credentials in prompts or files. <br>
Risk: SUNO_BASE_URL can redirect requests to a custom endpoint. <br>
Mitigation: Keep SUNO_BASE_URL unset for the default service or pin it to a trusted endpoint before running the skill. <br>
Risk: The artifact includes local-file upload behavior that can send explicitly selected media files to a remote service. <br>
Mitigation: Do not use upload-file or upload-based commands with sensitive local files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kennedydqz-del/suno-music-skill) <br>
- [Suno API documentation](https://docs.sunoapi.org/cn/suno-api/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API Calls, Text] <br>
**Output Format:** [Markdown with inline bash commands and JSON or text API output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SUNO_API_KEY and may return remote media URLs for generated audio and cover art.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
