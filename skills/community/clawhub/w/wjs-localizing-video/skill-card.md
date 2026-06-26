## Description: <br>
Thin orchestrator for an end-to-end video localization pipeline that routes full transcribe, translate, dub, and subtitle burn or mix requests to four focused sub-skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jianshuo](https://clawhub.ai/user/jianshuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and media-production users use this skill when they want an agent to coordinate full video localization, including transcription, subtitle translation, optional target-language dubbing, and final subtitle burn-in or audio mixing. The skill is intended for whole-pipeline requests rather than isolated transcription, translation, dubbing, or subtitle-rendering tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may use an automatically downloaded third-party ffmpeg binary when the local build lacks libass support. <br>
Mitigation: Prefer a reviewed and pinned ffmpeg build from a trusted source, or disable automatic downloads and provide a known-good local binary. <br>
Risk: The orchestrator delegates core work to sub-skills that are referenced but not included in this package. <br>
Mitigation: Review, install, and scan each referenced sub-skill before enabling the full localization pipeline. <br>
Risk: Localization can send transcript, subtitle, or speech-synthesis content to selected LLM, ASR, or TTS providers and may require sensitive TTS credentials. <br>
Mitigation: Use least-privilege credentials, keep secrets out of committed files, and process private videos only after confirming the data-handling posture of the configured providers. <br>


## Reference(s): <br>
- [Artifact README](README.md) <br>
- [Claude Code documentation](https://docs.claude.com/claude-code) <br>
- [Wjs Localizing Video ClawHub listing](https://clawhub.ai/jianshuo/wjs-localizing-video) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands, task checklists, file naming conventions, and generated SRT or MP4 file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Coordinates sub-skills that may produce source-language SRT files, translated SRT files, dubbed MP4 files, and final localized MP4 files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
