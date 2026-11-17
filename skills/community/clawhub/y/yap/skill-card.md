## Description:

Fast on-device speech-to-text using Apple Speech.framework (macOS 26+).

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobihagemann](https://clawhub.ai/user/tobihagemann)

### License/Terms of Use:


## Use Case:

Developers and end users use this skill to ask an agent for macOS speech-to-text commands that transcribe user-selected audio or video files with Apple's on-device Speech.framework.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a third-party Homebrew tap and CLI binary.

Mitigation: Review the tap and package provenance before installation when supply-chain assurance is required.

Risk: Transcription commands process local audio or video files selected by the user.

Mitigation: Run commands only on files intended for local CLI processing and review output destinations before saving transcripts.

Risk: The skill requires macOS 26 or later and installed Apple Speech models.

Mitigation: Confirm the target system and language models meet those requirements before relying on the generated commands.

## Reference(s):

- [yap project homepage](https://github.com/finnvoor/yap)
- [ClawHub skill page](https://clawhub.ai/tobihagemann/skills/yap)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include transcription command examples, locale options, output-format flags, and installation guidance for the required yap CLI.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
