## Description:

Publish Clean guides agents through UI theme customization for OpenClaw Control UI, DSH web UI, and other web projects, producing palettes, injection guidance, accessibility checks, and self-healing theme workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanhan1137](https://clawhub.ai/user/hanhan1137)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to plan and apply readable themed UI skins for OpenClaw Control UI, DSH web UI, or static web projects. It helps derive CSS tokens, validate contrast, prepare injection snippets and snapshots, and maintain or restore themes after app updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can add persistent daily execution that rewrites UI build files and crontab entries.

Mitigation: Review the self-healing flow before installation, back up the crontab, and make the cron step explicit and opt-in when persistence is not required.

Risk: Snapshot HTML or JavaScript can be reinserted into the Control UI after updates.

Mitigation: Inspect snapshot files before use, verify theme fingerprints, keep index.html backups, and run syntax plus visual checks after reinjection.

Risk: External style research or asset guidance can lead to untrusted tools or unclear asset rights if followed without review.

Mitigation: Use official or authorized asset channels, keep user-supplied assets out of released skill packages, and review third-party tools before installation.

## Reference(s):

- [Minecraft Worked Example](references/minecraft-example.md)
- [Open Source Checklist](references/open-source-checklist.md)
- [Pixel Game Style Guide](references/styles/pixel-game.md)
- [Cyberpunk Style Guide](references/styles/cyberpunk.md)
- [Cartoon Cute Style Guide](references/styles/cartoon-cute.md)
- [Minimal Modern Style Guide](references/styles/minimal-modern.md)
- [Dark Tech Style Guide](references/styles/dark-tech.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline CSS, HTML, JavaScript, shell commands, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include theme package file names, contrast-check results, snapshot instructions, and cron self-healing commands.]

## Skill Version(s):

1.5.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
