## Description: <br>
VoxFlow voice and AI-video CLI supports text-to-speech, podcasts, transcription, subtitle translation, dubbing, video translation, Slice card videos, and short-form AI clips. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chicogong](https://clawhub.ai/user/chicogong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run VoxFlow CLI workflows for speech synthesis, podcasts, transcription, translation, dubbing, video localization, and short-form media generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a VoxFlow account, quota-based cloud media processing, and locally stored authentication tokens. <br>
Mitigation: Confirm account use and quota-consuming commands before execution, check quota with voxflow status, and keep VOXFLOW_TOKEN out of logs and committed configuration. <br>
Risk: The artifact instructs agents to upgrade installed tooling and perform bulk skill installation without clear user confirmation. <br>
Mitigation: Require explicit user confirmation before upgrades, avoid unpinned latest installs, and prefer the pinned package from the ClawHub install metadata. <br>
Risk: The artifact can guide agents to submit GitHub issues that may include system details or user-provided content. <br>
Mitigation: Review issue text and any included environment details with the user before submitting. <br>


## Reference(s): <br>
- [VoxFlow homepage](https://voxflow.studio) <br>
- [VoxFlow CLI docs](https://voxflow.studio/docs/cli) <br>
- [VoxFlow skills docs](https://voxflow.studio/docs/skills) <br>
- [ClawHub Voxflow release](https://clawhub.ai/chicogong/voxflow) <br>
- [Deck Schema](references/deck-schema.md) <br>
- [Example Decks](references/example-decks.md) <br>
- [Slice Themes](references/themes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands, plus CLI-produced media or structured files depending on the workflow.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The VoxFlow CLI can produce audio, video, subtitles, transcripts, JSON decks, PPTX, PNG, and HTML artifacts.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
