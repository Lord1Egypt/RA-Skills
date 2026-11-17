## Description:

Organize, tag, search, and manage screenshots on macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[10oss](https://clawhub.ai/user/10oss)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find, organize, rename, archive, and search macOS screenshots, including OCR-based content search and CleanShot X workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screenshot cleanup and archive workflows may move or delete files unexpectedly.

Mitigation: Use dry runs and folder previews before applying changes, and keep backups before enabling cleanup rules.

Risk: OCR workflows may index private information contained in screenshots.

Mitigation: Avoid OCR indexing for sensitive screenshot folders and review generated indexes before sharing or storing them broadly.

Risk: CleanShot X cloud upload workflows may expose screenshots outside the local device.

Mitigation: Disable automatic cloud upload for sensitive captures and confirm sharing settings before generating links.

Risk: Changing the macOS screenshot save location is a persistent system preference change.

Mitigation: Confirm the intended destination folder before applying the preference change and document how to revert it.

## Reference(s):

- [Skreenshot ClawHub Skill Page](https://clawhub.ai/10oss/skills/skreenshot)
- [OCR Setup for Screenshot Search](references/ocr-setup.md)
- [CleanShot X Workflows](references/cleancast-x.md)
- [Automation Patterns](references/automation-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include local file-management commands, OCR setup steps, and optional automation workflows.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
