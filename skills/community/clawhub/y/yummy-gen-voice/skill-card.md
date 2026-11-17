## Description:

Use when the user wants to synthesise speech or text-to-speech (TTS) audio with Gemini through yummycli, including single-speaker narration, multi-speaker dialogue (up to 2 speakers), and listing available voices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yummysource](https://clawhub.ai/user/yummysource)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to synthesize Gemini text-to-speech audio through yummycli for narration, voiceovers, and two-speaker dialogue. The skill helps map user intent to model, voice, language, speaker, and output-path parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided text, speaker names, voices, or output paths could be mishandled if interpolated into shell strings.

Mitigation: Pass these values as literal process arguments and avoid constructing shell command strings from user input.

Risk: The skill installs and invokes an unpinned yummycli executable dependency.

Mitigation: Install only after trusting the @yummysource/yummycli package, and pin or verify the package version where deployment policy requires it.

Risk: Gemini credentials and generated audio may contain sensitive material.

Mitigation: Use approved Gemini credential handling and choose explicit output paths for sensitive audio files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yummysource/skills/yummy-gen-voice)
- [ClawHub publisher profile](https://clawhub.ai/user/yummysource)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with bash command examples and JSON command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated speech commands return JSON that includes the output .wav file path.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
