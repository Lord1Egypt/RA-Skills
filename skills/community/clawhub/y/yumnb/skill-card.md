## Description:

Yum NoteBook turns URLs, YouTube videos, screenshots, or text into a local notebook packet with source capture, summary notes, a dual-host MP3, a PowerPoint deck, and optional delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yumyumtum](https://clawhub.ai/user/yumyumtum)

### License/Terms of Use:

MIT

## Use Case:

Developers, students, and knowledge workers use this skill to have an agent capture a source and create an inspectable local notebook folder with notes, audio, slides, and links. It is suited for study notes, article or video recap workflows, and source-grounded presentation material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional AI, upload, webhook, and delivery integrations can send source content or generated artifacts to external services.

Mitigation: Keep ai.provider, upload.provider, notify.webhook_url, and deliver.provider disabled for sensitive sources unless external sharing is intended.

Risk: Configured helper commands or Python files can execute local programs.

Mitigation: Enable ai.cli.command, --fetcher, rclone/openclaw binaries, or onedrive_graph.uploader_path only when the referenced files and commands are trusted and protected from modification.

Risk: URL ingest may reach services available from the host machine.

Mitigation: Avoid URL ingest on machines that can access sensitive internal services.

## Reference(s):

- [Yum NoteBook ClawHub page](https://clawhub.ai/yumyumtum/skills/yumnb)
- [README.md](README.md)
- [rclone documentation](https://rclone.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Local files including Markdown summaries, plain-text talk-show scripts, MP3 audio, PowerPoint decks, JSON manifests, and captured source material.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates one timestamped output folder per request; upload, webhook notification, and direct delivery are optional and configuration-controlled.]

## Skill Version(s):

0.1.1 (source: server release evidence and RELEASE_NOTES_v0.1.1.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
