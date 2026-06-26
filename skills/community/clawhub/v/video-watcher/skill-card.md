## Description: <br>
Analyze video content by extracting frames at regular intervals for review, scene understanding, and description of common video formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kartinW](https://clawhub.ai/user/kartinW) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to inspect video files by extracting still frames, then sampling those frames to understand scenes, text, UI elements, actions, or transitions when direct video playback is not available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video content is converted into still image files in the workspace, which can expose sensitive frames after analysis. <br>
Mitigation: Use a dedicated output folder for sensitive videos and clean up extracted frames after review. <br>
Risk: Using an existing output folder can overwrite or mix with frame_*.jpg files that need to be kept. <br>
Mitigation: Choose a fresh output directory for each extraction and avoid reusing folders containing important frame files. <br>
Risk: The skill depends on ffmpeg being installed locally. <br>
Mitigation: Install ffmpeg only from trusted package managers before running the extraction script. <br>


## Reference(s): <br>
- [Skill source](artifact/SKILL.md) <br>
- [Frame extraction script](artifact/scripts/extract_frames.sh) <br>
- [ClawHub skill page](https://clawhub.ai/kartinW/video-watcher) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated JPEG frame files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ffmpeg and writes extracted frame images to a workspace output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
