## Description:

Finds and replaces literal or regex text across files, previewing matches by default and making per-file backups before applied changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT (code only; documentation and theory excluded)

## Use Case:

Developers and other users can preview bulk text matches across selected files, then apply literal or regex replacements when the results look right.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad glob with --apply can rewrite every matched file.

Mitigation: Preview first, choose a narrow glob, and check the affected files before applying changes; retain backups for recovery.

Risk: The declared permissions understate the local file and command access required.

Mitigation: Grant only the file and command access needed for the intended replacement and review the permission metadata before installation.

## Reference(s):

- [text-replace on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/text-replace)

## Skill Output:

**Output Type(s):** [Text, JSON, Files]

**Output Format:** [Plain-text or JSON match summary; updated files and .bak backups when applied]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to preview without writing; --apply modifies matching files after creating .bak backups.]

## Skill Version(s):

1.0.4 (source: ClawHub server-resolved release; bundled SKILL.md states 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
