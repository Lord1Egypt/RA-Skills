## Description: <br>
Converts website URLs into promotional videos using Remotion and React, including content extraction, animation setup, narration, subtitles, background music, and VPS-optimized rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffli2002](https://clawhub.ai/user/jeffli2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to turn a public website URL into a 60-second promotional video project with generated narration, subtitles, background music, screenshots, and local render commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches target websites and may be pointed at private or internal URLs. <br>
Mitigation: Use public intended URLs only and avoid private, internal, or sensitive endpoints. <br>
Risk: Generated projects install npm dependencies and run local render commands. <br>
Mitigation: Review generated files and package scripts before installing dependencies or running render commands. <br>
Risk: The project initializer downloads a background music file from an external URL. <br>
Mitigation: Confirm the downloaded media source and licensing before including it in a published video. <br>
Risk: Unvalidated brand names are used in generated file and package names. <br>
Mitigation: Use a simple alphanumeric brand name as recommended by the security guidance. <br>


## Reference(s): <br>
- [Component Template](artifact/references/component-template.tsx) <br>
- [URL to Video Generator on ClawHub](https://clawhub.ai/jeffli2002/url2video) <br>
- [Pixabay Background Music Asset](https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=electronic-future-beats-117998.mp3) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash, TypeScript, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to create a local Remotion project, narration text, optional audio assets, still images, and an MP4 render output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
