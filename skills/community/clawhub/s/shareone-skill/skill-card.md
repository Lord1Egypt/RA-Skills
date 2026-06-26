## Description: <br>
Publishes local HTML, Markdown, TXT, PDF, Word, or PPTX content to ShareOne to create public share links, and helps download, update, or process comments for existing ShareOne links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beep879](https://clawhub.ai/user/beep879) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to publish generated files or conversation content to ShareOne, manage sharing settings such as passwords, watermarks, custom slugs, and comments, and retrieve or update existing ShareOne links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses API-key based access for ShareOne actions. <br>
Mitigation: Prefer Sudowork or secret-store credential handling, avoid debug helpers that print keys, and rotate any key that appears in logs. <br>
Risk: Publishing actions can make local content externally accessible. <br>
Mitigation: Before publishing, verify the exact content to upload and confirm whether the resulting link should be public, password-protected, watermarked, or comment-enabled. <br>
Risk: Owner-authenticated operations can update existing shares and handle comments on behalf of the link owner. <br>
Mitigation: Use the intended ShareOne account and API key, preserve the target share identifier when updating, and review settings changes before execution. <br>


## Reference(s): <br>
- [Shareone Skill on ClawHub](https://clawhub.ai/beep879/skills/shareone) <br>
- [Skill Instructions](SKILL.md) <br>
- [Environment and Credentials Workflow](workflows/environment-and-credentials.md) <br>
- [Publish Text Page Workflow](workflows/publish-text-page.md) <br>
- [Publish Binary File Workflow](workflows/publish-binary-file.md) <br>
- [Download File Workflow](workflows/download-file.md) <br>
- [Comments Processing Workflow](workflows/comments-process.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Node.js command examples and JSON or status outputs from ShareOne scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce ShareOne share URLs, downloaded files, updated share settings, comment replies, and credential setup prompts.] <br>

## Skill Version(s): <br>
1.2.2 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
