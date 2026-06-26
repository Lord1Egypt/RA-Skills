## Description: <br>
Automated video production studio using Remotion, React, and TTS to create animated explainer videos from JSON content scripts through a make-driven pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hzsunzixiang](https://clawhub.ai/user/hzsunzixiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to scaffold Remotion video projects, configure narration and animation settings, and run a make-based pipeline that generates narrated explainer videos with subtitles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local Qwen TTS path can execute shell commands built from editable project configuration. <br>
Mitigation: Inspect project configuration and content inputs before running Qwen targets, especially conda environment names, venv paths, and custom config or content arguments. <br>
Risk: The skill runs a local build and render toolchain using make, npm, Python, ffmpeg, Remotion, and TTS tools. <br>
Mitigation: Review generated project files and run commands only in a trusted workspace with expected dependencies installed. <br>
Risk: Edge TTS sends narration text to an online TTS service. <br>
Mitigation: Use Edge TTS only when sending the narration text to the online service is acceptable; use the local Qwen path for offline synthesis when appropriate. <br>


## Reference(s): <br>
- [Animation Components Reference](artifact/references/animation-components.md) <br>
- [Configuration Reference](artifact/references/config-reference.md) <br>
- [Remotion Core Rules Reference](artifact/references/remotion-rules.md) <br>
- [Skill page](https://clawhub.ai/hzsunzixiang/remotion-video-studio) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration, TypeScript/React code, and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent through scaffolding and rendering a Remotion video project; the project pipeline produces audio assets, render props, subtitles, and a video file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
