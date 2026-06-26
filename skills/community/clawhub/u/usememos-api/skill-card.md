## Description: <br>
Interact with a UseMemos instance, a lightweight self-hosted memo hub, to create, search, list, comment on, and attach files to memos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minstn](https://clawhub.ai/user/minstn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to operate a configured UseMemos instance from an AI agent, including creating and finding memos, managing comments, and uploading or linking attachments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify memos, comments, and attachments on the configured UseMemos instance using the user's token. <br>
Mitigation: Install only when agent access to that instance is intended, and use an expiring or least-privilege token where possible. <br>
Risk: A local .env file stores the UseMemos URL and token for script execution. <br>
Mitigation: Keep the .env file private and avoid committing or sharing it. <br>
Risk: Attachment upload commands can send local files to the configured UseMemos instance. <br>
Mitigation: Review file paths before upload commands run. <br>
Risk: PUBLIC memo visibility and comment deletion can expose or remove content if used unintentionally. <br>
Mitigation: Avoid PUBLIC visibility unless intended, and confirm comment IDs before delete commands. <br>


## Reference(s): <br>
- [UseMemos API Reference](references/api.md) <br>
- [UseMemos](https://usememos.com) <br>
- [ClawHub skill page](https://clawhub.ai/minstn/usememos-api) <br>
- [Publisher profile](https://clawhub.ai/user/minstn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses USEMEMOS_URL and USEMEMOS_TOKEN to call the configured UseMemos API.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
