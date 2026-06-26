## Description: <br>
Video Pipeline turns natural-language prompts into short AI industry explainer videos using DashScope, text-to-speech, Remotion, and FFmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liwiw](https://clawhub.ai/user/liwiw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Content creators, developers, and business teams use this skill to generate 5-6 minute vertical or horizontal industry videos from a topic prompt, including outline, narration, visuals, TTS audio, timing alignment, and Remotion rendering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, outlines, and narration may be sent to external AI services. <br>
Mitigation: Avoid entering confidential or regulated content unless the DashScope account, terms, and data handling controls are approved for that use. <br>
Risk: The skill reads sensitive API credentials and evidence reports a hard-coded fallback API key. <br>
Mitigation: Use a user-controlled DashScope credential file, remove or rotate the fallback key before running the skill, and keep credentials out of generated project files. <br>
Risk: The pipeline can modify and delete files in a local Remotion project. <br>
Mitigation: Run it in an isolated project directory, review configured paths before execution, and keep backups or version control for generated assets. <br>
Risk: Generated narration or visuals may contain unsupported claims or misleading AI-generated content. <br>
Mitigation: Review generated outlines, narration, data claims, and final video before publication, especially for medical, financial, legal, or other high-impact topics. <br>
Risk: Unpinned dependencies and local rendering tools can change behavior across environments. <br>
Mitigation: Install in a dedicated environment, pin Python and Node package versions, and verify FFmpeg, Remotion, and TTS behavior before production use. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/liwiw/video-pipeline) <br>
- [Setup guide](setup_guide.md) <br>
- [Bug log](references/buglog.md) <br>
- [Node.js](https://nodejs.org/) <br>
- [Python](https://python.org/) <br>
- [FFmpeg](https://ffmpeg.org/download.html) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Python commands and generated project files, including JSON outlines and narration, HTML courseware, TSX Remotion components, MP3 audio, subtitles, and rendered video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local Remotion project, FFmpeg, Node.js, Python dependencies, and DashScope credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
