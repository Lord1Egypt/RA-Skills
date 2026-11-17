## Description:

Converts webpage content into a two-speaker Chinese podcast audio file using content summarization, dialogue drafting, TTS synthesis, and audio merging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangjinghua0127](https://clawhub.ai/user/yangjinghua0127)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to turn a source URL into a structured Chinese podcast package, including a source brief, dialogue draft, script JSON, and final MP3.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated podcast lines and Volc TTS credentials are sent to ByteDance TTS.

Mitigation: Use only with content and credentials approved for that external service.

Risk: Each run is instructed to clear prior files in the skill workspace.

Mitigation: Run it only in the intended skill workspace and keep important files outside skills/podcast-maker/workspace.

Risk: TTS request construction may be fragile for sensitive or untrusted source pages.

Mitigation: Harden TTS request generation with a JSON serializer before using sensitive or untrusted input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangjinghua0127/skills/url2podcast)
- [ByteDance Volcano Engine TTS API endpoint](https://openspeech.bytedance.com/api/v1/tts)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Audio files]

**Output Format:** [Markdown guidance with JSON artifacts, shell command snippets, WAV chunks, and an MP3 audio file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ffmpeg, curl, python3, VOLC_APPID, and VOLC_TOKEN; sends generated podcast lines to ByteDance TTS.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
