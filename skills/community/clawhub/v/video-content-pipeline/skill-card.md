## Description:

Faceless video production for YouTube, TikTok, and Shorts using generated scene images, parallax effects, voiceover, and ffmpeg composition, with scene prompts sent to Pollinations and narration text sent to Microsoft Edge TTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[northcap-group](https://clawhub.ai/user/northcap-group)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-production agents use this skill to turn a written script into scene JSON, generated images, narration audio, and a composed MP4 for faceless short-form video workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scene prompts and narration text are sent to third-party cloud services.

Mitigation: Do not use confidential or sensitive prompts or narration unless the user accepts those service disclosures.

Risk: The optional scene_gen.py path can make a paid x402 API call and may share the topic and API key with the configured endpoint.

Mitigation: Use it only when X402_API_KEY and X402_BASE are intentionally configured and possible charges and data sharing are accepted.

Risk: The compositor uses temporary files under /tmp on shared machines.

Mitigation: Avoid running composition in sensitive shared environments until temporary-file handling is hardened.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/northcap-group/skills/video-content-pipeline)
- [Pollinations image service](https://image.pollinations.ai)
- [Microsoft Edge TTS service endpoint](https://speech.platform.bing.com)
- [x402 API repository for optional paid scene generation](https://github.com/MohamedAbdisamed/x402-api)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Code, Files, Guidance]

**Output Format:** [Markdown guidance with bash commands; scripts produce JSON, PNG, MP3, and MP4 files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and ffmpeg; network calls may be made to Pollinations, Microsoft Edge TTS, and the optional configured x402 endpoint.]

## Skill Version(s):

1.0.16 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
