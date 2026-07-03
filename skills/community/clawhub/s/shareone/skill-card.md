## Description: <br>
Publishes local files or generated content to ShareOne as public share links, and helps agents download existing ShareOne links, update shared content or settings, and view or process comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beep879](https://clawhub.ai/user/beep879) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, employees, and external agents use this skill to publish HTML, Markdown, text, PDF, Word, PowerPoint, image, zip, or conversation content to ShareOne and return a shareable link. They can also retrieve ShareOne content, update share metadata such as password, watermark, short link, and comments, and close the loop on page comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A ShareOne API key used with this skill can publish, download, edit settings, and process comments. <br>
Mitigation: Use a managed secret store where available, avoid pasting long-lived keys into chat, and remove or rotate keys when access is no longer needed. <br>
Risk: Downloads may use saved owner credentials and bypass public share restrictions such as password or download settings. <br>
Mitigation: Confirm whether owner-privileged access is intended before relying on downloaded content, and run the skill without saved credentials for ordinary public-download checks. <br>
Risk: Publishing creates public ShareOne links for user-provided content. <br>
Mitigation: Require explicit user confirmation before first-time public publishing and review content for sensitive, unlawful, or malicious material before upload. <br>


## Reference(s): <br>
- [ClawHub ShareOne Skill Page](https://clawhub.ai/beep879/skills/shareone) <br>
- [ShareOne Skill Entrypoint](artifact/SKILL.md) <br>
- [Environment and Credentials Workflow](artifact/workflows/environment-and-credentials.md) <br>
- [Text Publishing Workflow](artifact/workflows/publish-text-page.md) <br>
- [Binary Publishing Workflow](artifact/workflows/publish-binary-file.md) <br>
- [Download Workflow](artifact/workflows/download-file.md) <br>
- [Comment Processing Workflow](artifact/workflows/comments-process.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands, script output summaries, and file or link results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create or update public ShareOne links, save downloaded files locally, and provide credential-handling prompts when required.] <br>

## Skill Version(s): <br>
1.2.3 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
