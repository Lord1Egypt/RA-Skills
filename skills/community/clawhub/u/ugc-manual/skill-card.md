## Description: <br>
Generate lip-sync video from an image and the user's own audio recording. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PauldeLavallaz](https://clawhub.ai/user/PauldeLavallaz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content operators use this skill to create lip-sync MP4 videos from a face image and a supplied audio recording when exact audio timing should be preserved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected face images and audio recordings are sent to ComfyDeploy for processing. <br>
Mitigation: Use only media appropriate for third-party processing, avoid highly sensitive or non-consensual face and voice media, and use a limited ComfyDeploy API key when possible. <br>
Risk: Remote audio URLs are downloaded and decoded locally before upload. <br>
Mitigation: Prefer local trusted files or trusted URLs, and install ffmpeg from a trusted source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PauldeLavallaz/ugc-manual) <br>
- [ComfyDeploy deployment queue API endpoint](https://api.comfydeploy.com/api/run/deployment/queue) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [MP4 video file with command-line progress text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires COMFY_DEPLOY_API_KEY and ffmpeg; converts audio to WAV PCM 16-bit mono 48kHz before workflow submission.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
