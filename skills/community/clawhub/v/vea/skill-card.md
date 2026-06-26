## Description: <br>
Video Editing Agent (VEA) supports automated video processing, video indexing, highlight generation, narration, subtitles, background music selection, and AI-powered clip selection for long-form video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawnshenopeninterx](https://clawhub.ai/user/shawnshenopeninterx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and video operations teams use this skill to run a local VEA service that indexes source videos, answers questions about indexed media, and generates edited outputs such as highlight reels, shorts, narration, subtitles, background music mixes, and Final Cut Pro XML. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow requires credentials for Memories.ai, Google, ElevenLabs, and optionally Soundstripe, and those services may receive selected video frames, text, transcripts, or generated media data. <br>
Mitigation: Use dedicated least-privilege API keys, confirm each processing job before sending media to external services, and rotate or revoke credentials after sensitive projects. <br>
Risk: Installation uses an external GitHub repository and uv installer before the local VEA service is run. <br>
Mitigation: Inspect and pin the external repository and installer before running them in an isolated environment. <br>
Risk: Edited videos, indexes, clip plans, narrations, subtitles, and music files are stored locally after processing. <br>
Mitigation: Delete local outputs and indexing directories after handling sensitive media, and restrict filesystem access to the VEA workspace. <br>
Risk: Broad Google application-default credentials can expose more access than the workflow needs. <br>
Mitigation: Prefer project-scoped service credentials or narrowly scoped keys instead of broad personal application-default credentials. <br>


## Reference(s): <br>
- [VEA API Reference](references/api.md) <br>
- [VEA Configuration](references/config.md) <br>
- [VEA Open Source Repository](https://github.com/Memories-ai-labs/vea-open-source) <br>
- [VEA Paper](https://arxiv.org/abs/2509.16811) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown guidance with API examples, JSON request bodies, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated video workflows may produce local files such as MP4 outputs, clip plans, narration audio, subtitles, music files, and FCPXML project files through the VEA service.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
