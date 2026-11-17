## Description:

Converts user-provided text and documents into expressive MP3 narration while preserving the source content and validating the merged audio with FFmpeg/FFprobe.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ciklopentan](https://clawhub.ai/user/ciklopentan)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill to turn supplied text into checked MP3 narration for read-aloud workflows, audiobook-style output, and voice-over drafts. It is intended for ChatGPT Work/Codex-style browser-assisted TTS workflows and local audio merging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text sent to browser-based TTS services may be processed by remote providers.

Mitigation: Do not submit private, confidential, credential-like, or personal text to remote TTS unless the user explicitly approves; prefer a local TTS path for sensitive content.

Risk: Browser TTS providers can change limits, availability, quotas, voices, or output behavior.

Mitigation: Recheck the selected provider's current limits and generation status before each job, avoid repeated failed routes, and verify that every segment was generated and downloaded once.

Risk: Short, missing, reordered, or incompatible audio segments can produce an incomplete final MP3.

Mitigation: Preserve segment order, compare expected and actual duration, require compatible MP3 parameters, and decode-check the final file with FFmpeg/FFprobe.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ciklopentan/skills/text-to-audio-gpt)
- [TTSFree Russian text-to-speech page](https://ttsfree.com/text-to-speech/ru)

## Skill Output:

**Output Type(s):** [files, shell commands, guidance]

**Output Format:** [MP3 audio file with concise Markdown status and JSON merge-check output when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one merged MP3 from ordered compatible MP3 segments; FFmpeg and FFprobe are required for local validation.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
