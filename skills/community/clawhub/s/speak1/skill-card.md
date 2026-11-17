## Description:

Text-to-speech using Kokoro local TTS. Use when the user wants to convert text to audio, read aloud, or generate speech.

This skill is ready for commercial/non-commercial use.

## Publisher:

[babysor](https://clawhub.ai/user/babysor)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use this skill to convert text, text files, EPUBs, and PDFs into local speech audio with Kokoro TTS, including voice selection, voice blending, streaming playback, and split chapter output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned kokoro-tts installation and downloaded model or voice files can introduce supply-chain uncertainty.

Mitigation: Pin the kokoro-tts package version and verify downloaded model and voice files before use.

Risk: Text, EPUB, or PDF inputs may contain sensitive content that will be processed by the local TTS environment.

Mitigation: Run the skill only in environments approved for the selected documents and avoid processing secrets or credentials unless that handling is acceptable.

## Reference(s):

- [Kokoro TTS Reference](artifact/reference.txt)
- [Kokoro TTS](https://github.com/nazdridoy/kokoro-tts)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of audio files or streaming playback through local kokoro-tts commands; Python 3.9-3.12 is required by the artifact reference.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
