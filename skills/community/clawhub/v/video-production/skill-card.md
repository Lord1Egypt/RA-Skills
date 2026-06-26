## Description: <br>
Complete A/B video pipeline for storyboarding, Veo 3 batch generation, browser preview with feedback, and ffmpeg assembly into final videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omerflo](https://clawhub.ai/user/omerflo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and production teams use this skill to generate multi-scene AI video projects, compare A/B hooks and CTAs, review generated clips, apply feedback, and assemble approved clips into final cuts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The quota watcher can add a recurring cron retry workflow that continues running in the background. <br>
Mitigation: Install the watcher only when needed, inspect crontab before and after use, and remove or disable the cron entry after quota recovery. <br>
Risk: Hardcoded local paths and a hardcoded notification recipient can send status updates or operate on the wrong project in another environment. <br>
Mitigation: Replace hardcoded paths and notification targets with user-reviewed configuration before running the workflow. <br>
Risk: Provider API keys are loaded from shell environment files and may be exposed by local shell or process practices. <br>
Mitigation: Store API keys in a safer secret mechanism and avoid committing or sharing shell files that contain credentials. <br>
Risk: Generated prompts, clips, logs, and reference assets can contain sensitive campaign or identity material. <br>
Mitigation: Set retention and deletion rules for generated media, logs, prompts, and reference assets before using the skill on sensitive projects. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/omerflo/video-production) <br>
- [Storyboard Template](references/storyboard-template.md) <br>
- [Veo 3 Platform Guide](references/platform-guide-veo3.md) <br>
- [Timing & Audio Synchronization Guide](references/timing-sync.md) <br>
- [Premiere Pro Export Settings](references/premiere-export.md) <br>
- [Google Cloud API credentials](https://console.cloud.google.com/apis/credentials) <br>
- [OpenAI API keys](https://platform.openai.com/api/keys) <br>
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with JSON storyboard and feedback formats, shell commands, Python scripts, generated preview HTML, MP4 clips, and final assembled video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided storyboard and feedback files, media assets, ffmpeg, and configured provider API keys for generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
