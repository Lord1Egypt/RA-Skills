## Description:

Creates dark motivational TikTok/Reels videos by generating a timed script, ElevenLabs voiceover, Pexels stock footage selection, MoviePy text overlays, FFmpeg color grading, and a 1080x1920 MP4 export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thuongvh2-python](https://clawhub.ai/user/thuongvh2-python)

### License/Terms of Use:


## Use Case:

Content creators, marketers, and developers use this skill to assemble short dark-aesthetic motivational videos for TikTok or Reels from generated scripts, synthetic voiceover, and real Pexels footage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote media downloads may be fetched and processed without strong host, content type, redirect, or size bounds.

Mitigation: Run the skill in an isolated environment with limited filesystem access and add explicit download validation before using it on sensitive machines.

Risk: Third-party Python dependencies are documented without pinned versions.

Mitigation: Pin and review dependency versions before installation or deployment.

Risk: The pipeline requires Anthropic, ElevenLabs, and Pexels API keys.

Mitigation: Use service-scoped API keys, store them outside the artifact, and rotate them if exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thuongvh2-python/skills/tiktok-motivation-video)
- [Publisher profile](https://clawhub.ai/user/thuongvh2-python)
- [Pexels API](https://www.pexels.com/api/)
- [Anthropic Messages API endpoint](https://api.anthropic.com/v1/messages)
- [ElevenLabs Text to Speech API endpoint](https://api.elevenlabs.io/v1/text-to-speech/{voice_id})
- [ElevenLabs voice catalog](artifact/elevenlabs_voices.md)
- [Complete runnable pipeline](artifact/pipeline_full.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python and shell command examples; when executed, the pipeline writes MP3, intermediate MP4, and final 1080x1920 MP4 files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Anthropic, ElevenLabs, and Pexels API keys plus FFmpeg and Python media dependencies.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
