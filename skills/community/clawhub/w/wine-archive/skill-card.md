## Description:

Store, recall, and manage personal wine tastings and label images through natural-language queries backed by a local SQLite archive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sidvorak](https://clawhub.ai/user/sidvorak)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to log, search, recall, export, import, and share a personal wine tasting archive, including archived label images and optional Telegram delivery. It supports local-first operation with optional LLM-based intent classification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted imports or label paths can expose arbitrary local files during import/export or Telegram label sending.

Mitigation: Review before installing, import only trusted archives, and avoid --include-images or Telegram label sending until image paths are constrained to the label directory.

Risk: Optional LLM intent classification may send message text to a model provider and store interactions locally.

Mitigation: Keep LLM classification disabled unless needed, configure provider keys deliberately, avoid sensitive inputs, and protect local interaction logs.

Risk: Export archives can contain personal tasting history and embedded label images.

Mitigation: Store and transfer exported archives as sensitive personal data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sidvorak/skills/wine-archive)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown and CLI-oriented text, with structured JSON for Telegram bridge actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local SQLite records, label image files, export archives, and audit logs.]

## Skill Version(s):

0.1.8 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
