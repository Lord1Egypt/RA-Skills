## Description:

Converts Markdown and text chapter files into MP3 audiobook audio using the Xiaomi MiMo TTS API, with batch processing, long-text segmentation, voice selection, and style controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouchang1988](https://clawhub.ai/user/zhouchang1988)

### License/Terms of Use:

MIT

## Use Case:

Developers and creators use this skill to convert directories of novel chapters into MP3 audiobook files through Xiaomi MiMo TTS. It supports chapter ranges, output directories, voice and style selection, request delay configuration, and resume behavior for existing audio files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends chapter text to a remote TTS provider.

Mitigation: Use it only with text that is appropriate to share with the configured Xiaomi MiMo endpoint.

Risk: API credentials may be exposed through command arguments or logs.

Mitigation: Prefer the MIMO_API_KEY environment variable and avoid pasting keys into shared shell history or transcripts.

Risk: Custom API base URLs can redirect text and credentials to an untrusted endpoint.

Mitigation: Use custom --base-url values only for endpoints that have been explicitly reviewed and trusted.

Risk: The wrapper script can execute injected shell commands when run with untrusted arguments.

Mitigation: Review and fix the command construction before running scripts/run.sh with untrusted input.

Risk: Dependencies are not pinned to exact versions.

Mitigation: Pin and review dependency versions before deployment in controlled or production environments.

## Reference(s):

- [Xiaomi MiMo Token Plan](https://mimo.mi.com/token-plan)
- [ClawHub skill page](https://clawhub.ai/zhouchang1988/skills/xiaomi-tts-chapters)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated MP3 audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a Xiaomi MiMo API key and sends chapter text to a remote TTS provider; API usage may incur costs.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
