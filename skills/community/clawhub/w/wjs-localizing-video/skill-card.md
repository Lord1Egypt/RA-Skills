## Description:

Wjs Localizing Video orchestrates end-to-end video localization by routing full-pipeline requests through transcription, subtitle translation, optional dubbing, and subtitle burn or mix sub-skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jianshuo](https://clawhub.ai/user/jianshuo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external video creators use this skill when they want an agent to run a complete video localization workflow, including transcription, subtitle translation, optional dubbing, and final subtitle rendering or audio mixing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The video rendering workflow may fetch an unverified third-party ffmpeg binary fallback.

Mitigation: Disable or review the evermeet ffmpeg fallback and prefer a trusted local ffmpeg build with libass support.

Risk: The workflow may run local media-processing commands, install Python dependencies, and use TTS credentials supplied by the user.

Mitigation: Run it in a controlled environment, pin dependencies, and provide only credentials intended for the target TTS service.

Risk: A hardcoded upload CTA rule may not match the user's channel or publication context.

Mitigation: Remove or update the CTA rule before combining the workflow with upload or publishing steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jianshuo/skills/wjs-localizing-video)
- [Claude Code documentation](https://docs.claude.com/claude-code)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [edge-tts](https://github.com/rany2/edge-tts)
- [Volcano Doubao speech synthesis documentation](https://www.volcengine.com/docs/6561/1598757)
- [evermeet ffmpeg builds](https://evermeet.cx/ffmpeg/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands and localized media or subtitle file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce SRT subtitle files and MP4 outputs through delegated transcription, translation, dubbing, and rendering sub-skills.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
