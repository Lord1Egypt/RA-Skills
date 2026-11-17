## Description:

Local Chinese text-to-speech skill based on Qwen3-TTS that helps agents convert text to speech, clone voices, design new voices, and generate dialogue voiceover audio through the SnowVoice CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[webkubor](https://clawhub.ai/user/webkubor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn Chinese text prompts into local speech audio, choose or clone existing personas, design new voice styles, and retrieve the generated output file path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs an unpinned remote installer from the SnowVoice upstream repository with broad user-level command authority.

Mitigation: Review before installing; only run setup after trusting the upstream repository, inspect the cloned installer first, and prefer a pinned, verified release.

Risk: Automatic setup could be triggered during a casual text-to-speech request.

Mitigation: Require explicit user confirmation before running setup or model downloads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/webkubor/skills/snowvoice-tts)
- [SnowVoice Studio project link declared by the skill](https://github.com/webkubor/snowvoice-studio)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code]

**Output Format:** [Markdown guidance with shell commands and JSON-style command results that include generated audio file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can trigger local setup, model downloads, voice listing, voice cloning, and voice design; generated audio is written under the SnowVoice output directory.]

## Skill Version(s):

1.0.2 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
