## Description: <br>
Videogen is a video-account short-video production pipeline that plans scripts and storyboards, generates TTS narration and AI video clips, renders Remotion or presentation-style visuals, and assembles vertical videos with FFmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devioslang](https://clawhub.ai/user/devioslang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and developers use this skill to turn a topic, article URL, or video concept into a short-form vertical video workflow with script, storyboard, narration, rendered visuals, AI video clips, and final assembly commands. It is oriented toward WeChat Channels-style educational, narrative, and mixed explainer videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can fetch arbitrary URLs and send user-provided narration or source content to external AI, TTS, and video providers. <br>
Mitigation: Avoid private URLs and confidential material unless provider transmission is acceptable, and review prompts and extracted content before generation. <br>
Risk: The artifact can install Python or npm packages and invoke FFmpeg, npm, pip, and rendering commands. <br>
Mitigation: Run in a sandboxed workspace, review commands before execution, and regenerate package locks with HTTPS registries before installing dependencies. <br>
Risk: The pipeline may read MiniMax credentials from environment variables or a home-directory .env file. <br>
Mitigation: Use scoped credentials, keep secrets out of generated artifacts, and rotate keys if they may have been exposed during video generation. <br>


## Reference(s): <br>
- [ClawHub Videogen release page](https://clawhub.ai/devioslang/videogen) <br>
- [Apple-style Remotion template guide](artifact/templates/apple/README.md) <br>
- [Evaluation prompts](artifact/evals/evals.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance, JSON storyboard structures, Python and shell command examples, Remotion project files, and generated media file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces intermediate storyboard, script, narration, clip, render, subtitle, and final video artifacts under a minimax-output-style workspace.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
