## Description:

Qwen3-TTS local voice synthesis supports voice cloning, voice design, and multi-role dialogue, with fallback to Edge TTS through tts-cosyvoice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentlau2046-sudo](https://clawhub.ai/user/vincentlau2046-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to synthesize Chinese speech from text through local Qwen3-TTS voice presets, including cloned and designed character voices. It is suited for story narration, character dialogue, and workflows that need WAV output with optional fallback speech generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Speech text may leave the local machine through the configurable ComfyUI endpoint or automatic Edge TTS fallback.

Mitigation: Use only a trusted local ComfyUI endpoint and disable fallback with --fallback-edge false when text must remain local.

Risk: The package advertises a multi-role dialogue helper that is not included in the inspected files.

Mitigation: Treat multi-role dialogue support as unavailable until the missing helper is supplied and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vincentlau2046-sudo/skills/tts-qwen3)
- [Publisher profile](https://clawhub.ai/user/vincentlau2046-sudo)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, files]

**Output Format:** [Shell command guidance and generated audio files, with optional SRT path guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The inspected package includes a single-role TTS script; advertised multi-role dialogue helper behavior is not included in the package.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
