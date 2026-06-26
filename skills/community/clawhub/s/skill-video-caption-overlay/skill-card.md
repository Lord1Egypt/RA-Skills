## Description: <br>
Render TikTok-style animated pill captions onto short-form videos using MoviePy + PIL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and video creators use this skill to render styled caption overlays onto short-form videos for TikTok ads, Reels, and YouTube Shorts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may fetch MoviePy and Pillow through `uv`, which can reduce repeatability across environments. <br>
Mitigation: Pin dependency versions and review installed packages before production use. <br>
Risk: Default font paths may not exist outside the publisher's environment. <br>
Mitigation: Pass explicit `--font-black` and `--font-bold` paths for available TrueType fonts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zero2Ai-hub/skill-video-caption-overlay) <br>
- [Publisher profile](https://clawhub.ai/user/Zero2Ai-hub) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>
- [Example captions JSON](artifact/scripts/example_captions.json) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for a local Python media-rendering workflow that outputs an MP4 video file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
