## Description: <br>
Generates two-host podcast audio from a topic or script using SenseAudio TTS, with optional LLM script generation, voice selection, cloned or text-generated voices, and speed and pitch controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cowboy231](https://clawhub.ai/user/cowboy231) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to turn a topic or prepared script into an MP3 podcast, either through a local web UI or through chat workflows for IM channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill starts local services and depends on hard-coded local paths and a Flask endpoint on port 5000. <br>
Mitigation: Review the local service behavior before installing, prefer local-only generation, and update paths and service configuration for the deployment environment. <br>
Risk: The skill reads SenseAudio, OpenClaw gateway, and Feishu credentials from local configuration. <br>
Mitigation: Provide only the credentials needed for the selected workflow, keep secrets out of prompts and logs, and document required credentials before broad use. <br>
Risk: Generated audio can be uploaded to Feishu cloud storage without tight user control. <br>
Mitigation: Avoid Feishu mode unless the account and destination folder are explicitly approved, make cloud upload opt-in, and verify external destinations before sharing files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cowboy231/senseaudio-podcast-generator) <br>
- [SenseAudio homepage](https://senseaudio.cn) <br>
- [Agent usage guide](artifact/references/AGENT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance, JSON command results, shell commands, and generated MP3 audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SENSEAUDIO_API_KEY and FFmpeg; local mode starts a Flask service on port 5000; IM workflows may prepare or upload generated audio for delivery.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
