## Description:

QQ Zone Photo helps agents manage QQ Zone albums, including QR-code login, album listing, photo browsing, uploads, downloads, and album creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent operate QQ Zone photo albums through natural-language requests such as backing up albums, uploading photos, browsing album contents, and creating albums.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: QQ cookies can grant broad access to a user's QQ Zone albums.

Mitigation: Use a dedicated cookies.json file, keep it private, avoid sharing it, and refresh credentials if exposure is suspected.

Risk: The skill can perform account-changing or bulk actions such as uploads, album creation, and full-album downloads.

Mitigation: Confirm the target account, album, files, and destination before allowing commands to run.

Risk: The security verdict is suspicious because requested behavior has broader authority than the manifest declares.

Mitigation: Review the skill before installation and run it only when explicit QQ Zone album access or changes are intended.

## Reference(s):

- [QQ Zone Photo ClawHub Page](https://clawhub.ai/thcjp/skills/qq-zone-photo-free)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides album actions and command parameters; some workflows rely on a local cookies.json file.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
