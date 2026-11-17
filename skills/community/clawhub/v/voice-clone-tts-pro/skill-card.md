## Description:

Voice Clone helps agents synthesize speech and produce voice-clone style audio with selectable TTS engines, voices, languages, rate, pitch, and tone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxliuyu](https://clawhub.ai/user/sxliuyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to convert supplied text into spoken audio, select voice and language settings, and save the resulting audio locally for multilingual narration or voice synthesis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports a command-injection flaw related to opening generated files.

Mitigation: Review before installing, avoid untrusted output paths, and replace shell-based playback with a non-shell subprocess call or make playback opt-in.

Risk: Cloud TTS providers may receive sensitive text or voice material, and the artifact under-discloses this data handling.

Mitigation: Do not use sensitive text or unauthorized voice material, and add clear privacy and consent guidance before deployment.

Risk: Dependencies are not pinned, which can change runtime behavior or security exposure over time.

Mitigation: Pin and review dependencies before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sxliuyu/skills/voice-clone-tts-pro)

## Skill Output:

**Output Type(s):** [Audio files, Text, Shell commands, Configuration guidance]

**Output Format:** [Local audio files with command-line status text and Markdown usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated audio is saved locally; some engines require API keys and may send text or voice data to cloud services.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
