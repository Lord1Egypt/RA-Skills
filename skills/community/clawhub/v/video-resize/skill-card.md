## Description: <br>
Use when the user wants to change a video's aspect ratio or reformat it for a specific platform using a local ffmpeg center-crop workflow, with optional guidance to use AI Edit for subject-aware smart cropping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Symbolk](https://clawhub.ai/user/Symbolk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and external users use this skill to reformat videos for common platform aspect ratios such as 9:16, 1:1, 16:9, 4:3, and 21:9. It is intended for local resizing with ffmpeg when a center crop is acceptable, with separate guidance for AI-assisted subject-aware editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI Edit can upload videos and prompts to a remote service. <br>
Mitigation: Use local scripts/resize.sh for private videos, and use AI Edit only after explicitly approving the upload workflow and the destination service. <br>
Risk: The resize script invokes ffmpeg with overwrite enabled and can replace an existing output file. <br>
Mitigation: Choose a fresh output filename or confirm that replacing the target file is acceptable before running the script. <br>
Risk: Local resizing uses a center crop and may remove important off-center content. <br>
Mitigation: Preview the resized output and switch to subject-aware editing when the important subject is not centered. <br>


## Reference(s): <br>
- [Video Resize ClawHub release](https://clawhub.ai/Symbolk/video-resize) <br>
- [Sparki homepage](https://sparki.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with bash commands; the resize script writes a video file and prints the output path.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ffmpeg for local resizing; AI Edit guidance requires SPARKI_API_KEY and may return a temporary download URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
