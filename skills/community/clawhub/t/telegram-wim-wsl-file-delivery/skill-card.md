## Description:

Deliver local reports and artifacts through OpenClaw chat channels. Use when generated HTML/PDF/archive/table files must be sent from local, self-hosted, or WSL OpenClaw setups where host-read policy matters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pe4atnik](https://clawhub.ai/user/pe4atnik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deliver locally generated reports, archives, tables, and other artifacts from local, self-hosted, or WSL OpenClaw environments into Telegram or other configured chat channels while handling host-read path constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended to send local files through configured chat channels, so file contents may leave the machine.

Mitigation: Require explicit confirmation of the source path, destination, and user intent before sending, and report the resulting message id or send result.

Risk: The documented HTML workflow copies local HTML into OpenClaw's trusted temp directory before external delivery.

Mitigation: Use the trusted temp copy only for verified generated reports, check MIME type and file size first, and avoid arbitrary pre-existing HTML or sensitive files unless separately reviewed.

Risk: Host-read restrictions, wrapper payload bugs, path expansion, and channel size or compression behavior can cause failed or misleading sends.

Mitigation: Use absolute paths, verify files with ls and file, prefer the OpenClaw CLI fallback when wrapper sends fail, use --force-document when needed, and change one variable before retrying.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pe4atnik/skills/telegram-wim-wsl-file-delivery)
- [Debug Notes](references/debug-notes.md)
- [Positioning](references/positioning.md)
- [Comparison Notes](references/comparison-notes.md)
- [Skill Audit - 2026-06-23](references/skill-audit-2026-06-23.md)
- [Send HTML Report Example](examples/send-html-report.sh)
- [Send Archive Example](examples/send-archive.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw plus local shell tools: openclaw, file, cp, chmod, mkdir, node, and ls.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
