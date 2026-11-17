## Description:

Turn scripts into publishable voiceovers with Voice.ai TTS, including segments, chapters, captions, and video muxing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gizmogremlin](https://clawhub.ai/user/gizmogremlin)

### License/Terms of Use:

MIT

## Use Case:

External creators, content teams, and developers use this skill to turn Markdown or text scripts into creator voiceover assets with Voice.ai TTS. It can generate segmented audio, captions, chapters, review pages, metadata, and optional video audio replacement workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Voice.ai API base URL can be redirected through VOICEAI_API_BASE, which could send scripts and API credentials to an untrusted endpoint.

Mitigation: Leave VOICEAI_API_BASE unset unless the endpoint is trusted, and use a dedicated Voice.ai API key with appropriate access limits.

Risk: When ffmpeg is unavailable, the skill can generate helper shell or PowerShell scripts for later execution.

Mitigation: Review generated ffmpeg helper scripts and input/output paths before running them, especially when filenames or output paths are untrusted.

Risk: Script text is sent to Voice.ai for TTS generation during non-mock runs.

Mitigation: Avoid sending sensitive or confidential scripts unless the user is comfortable sharing that content with Voice.ai.

## Reference(s):

- [Voice.ai API Reference](references/VOICEAI_API.md)
- [Troubleshooting](references/TROUBLESHOOTING.md)
- [Voice.ai Developer API](https://dev.voice.ai/api/v1)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with CLI commands and generated project files such as WAV or MP3 audio, HTML review pages, SRT captions, JSON manifests, and text metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 20 or newer, a Voice.ai API key for real TTS calls, and ffmpeg for master stitching, MP3 encoding, normalization, and video muxing.]

## Skill Version(s):

0.1.3 (source: server release metadata; artifact frontmatter and package.json report 0.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
