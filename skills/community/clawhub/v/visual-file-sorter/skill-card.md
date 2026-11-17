## Description:

Visual File Sorter traverses a Downloads or Desktop folder, uses vision to inspect file contents, renames files, and archives them into sorted directories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anotherj1](https://clawhub.ai/user/anotherj1)

### License/Terms of Use:


## Use Case:

External users and local desktop users use this skill to organize cluttered Downloads or Desktop folders by visually identifying files, assigning descriptive names, and moving them into category directories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically open, visually inspect, rename, and move broad sets of files from Desktop or Downloads.

Mitigation: Run it only on a small backed-up folder and require a preview plus confirmation before opening, renaming, or moving each file.

Risk: Default-app opening can be unsafe for untrusted downloads or active file types.

Mitigation: Avoid untrusted downloads and skip active file types unless the workflow has been changed to use safer previews.

Risk: Limited user control can lead to incorrect renames or misplaced files.

Mitigation: Review proposed filenames and destination folders before applying any file operations.

## Reference(s):

- [Visual File Sorter ClawHub release](https://clawhub.ai/anotherj1/skills/visual-file-sorter)
- [Publisher profile: anotherj1](https://clawhub.ai/user/anotherj1)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown or text with shell commands and file-operation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute local file renaming and moving workflows; no deletion is described by the artifact.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
