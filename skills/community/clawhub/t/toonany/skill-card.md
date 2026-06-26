## Description: <br>
Toonany helps creators turn novels and stories into AI-generated short dramas through a guided pipeline for storylines, outlines, assets, scripts, storyboards, video, audio, subtitles, and final post-production. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[casperkwok](https://clawhub.ai/user/casperkwok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, developers, and media teams use Toonany to convert written stories into short-form visual drama projects and final video outputs. It supports staged control over style samples, character assets, storyboard images, video clips, narration, subtitles, and post-production. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Story text, prompts, reference images, dialogue, and generated media may be sent to configured external AI providers. <br>
Mitigation: Use only approved providers for the project and avoid processing confidential manuscripts or client material without permission. <br>
Risk: The skill requires sensitive API credentials and may incur provider costs. <br>
Mitigation: Store keys in environment variables or a secret manager, do not place secrets in project files, and review provider usage limits before running generation steps. <br>
Risk: Intermediate project files and exports can contain sensitive creative material. <br>
Mitigation: Keep project directories private, restrict sharing of exported bundles, and review generated files before distribution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/casperkwok/toonany) <br>
- [README](README.md) <br>
- [Tutorial](TUTORIAL.md) <br>
- [Workflow Reference](references/workflow.md) <br>
- [Commands Reference](references/commands.md) <br>
- [Model Configuration Guide](references/model-config.md) <br>
- [Data Model Reference](references/data-model.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON configuration, Shell commands, Media files, Guidance] <br>
**Output Format:** [Markdown, JSON project files, shell commands, image/audio/video files, and SRT subtitles] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured AI provider API keys and ffmpeg for final video assembly.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata; artifact frontmatter and changelog list 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
