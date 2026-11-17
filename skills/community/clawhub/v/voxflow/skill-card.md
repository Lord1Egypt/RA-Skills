## Description:

Slice helps agents use the VoxFlow CLI to create narrated media workflows, including text-to-speech audio, multi-speaker podcasts, transcripts, subtitle translation, dubbing, vertical Slice card videos, and short AI clips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chicogong](https://clawhub.ai/user/chicogong)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content creators use this skill to route an agent through VoxFlow media tasks such as reading text aloud, generating podcasts, transcribing or translating audio and video, dubbing subtitles, and preparing Slice card-video decks or renders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User media, transcripts, subtitles, and generated content may be processed through VoxFlow cloud services.

Mitigation: Review input data before sending it through the CLI and avoid sensitive or private media unless cloud processing is acceptable.

Risk: The skill includes global CLI installation and upgrade behavior.

Mitigation: Review and approve the exact install or upgrade command before execution; do not auto-upgrade, install voxflow@latest, or run broad skill installs without approval.

Risk: Diagnostic or issue-reporting workflows may submit information externally.

Mitigation: Review diagnostics and issue content before submission and remove secrets, personal data, or proprietary media details.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chicogong/skills/voxflow)
- [VoxFlow Homepage](https://voxflow.studio)
- [VoxFlow CLI Docs](https://voxflow.studio/docs/cli)
- [VoxFlow Skills Overview](https://voxflow.studio/docs/skills)
- [Slice App](https://voxflow.studio/apps/slice)
- [Slice Deck Schema](artifact/references/deck-schema.md)
- [Slice Themes](artifact/references/themes.md)
- [Slice Example Decks](artifact/references/example-decks.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON deck snippets, and file path instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in generated audio, video, transcript, subtitle, deck JSON, or image files when the agent runs approved VoxFlow CLI commands.]

## Skill Version(s):

1.3.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
