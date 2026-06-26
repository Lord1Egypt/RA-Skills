## Description: <br>
Generate and stitch short videos via Google Veo 3.x using the Gemini API (google-genai). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creators use this skill to generate short MP4 clips from prompts through Google Veo 3.x, with options to stitch segments, use reference images, and preserve continuity across longer videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected reference or last-frame images are sent to Google Gemini/Veo. <br>
Mitigation: Use a scoped GEMINI_API_KEY through the environment and avoid submitting confidential or regulated media. <br>
Risk: The script writes generated videos and temporary segment files to user-specified paths. <br>
Mitigation: Review --filename and segment options before running so files are written only where expected. <br>
Risk: Longer multi-segment videos depend on ffmpeg and external API quota or availability. <br>
Mitigation: Install ffmpeg before using --segments greater than 1, and retry or adjust the workflow when the API returns quota or availability errors. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zero2Ai-hub/skill-veo3-video-gen) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and local MP4 file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GEMINI_API_KEY; multi-segment output requires ffmpeg and writes MP4 files to user-specified paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
