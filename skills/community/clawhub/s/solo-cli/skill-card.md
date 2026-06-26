## Description: <br>
Monitor and interact with SOLO.ro accounting platform data through the solo-cli CLI or TUI, including summaries, revenues, expenses, queue items, e-Factura documents, company profile details, uploads, and safe command translation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rursache](https://clawhub.ai/user/rursache) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External SOLO.ro users and agent operators use this skill to translate accounting requests into solo-cli commands and inspect summaries, invoices, expenses, e-Factura documents, queue items, company details, and document upload or delete actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and uses an unpinned third-party CLI from rursache/tap/solo-cli. <br>
Mitigation: Install only if the publisher and Homebrew tap are trusted, and verify the source before use in sensitive accounting workflows. <br>
Risk: The CLI stores SOLO.ro credentials and session cookies locally. <br>
Mitigation: Protect the config and cookie files, use a custom config path when appropriate, and avoid exposing credentials in command arguments, logs, or chat transcripts. <br>
Risk: Upload and queue delete commands can change accounting documents or queues. <br>
Mitigation: Confirm the target account, file path, and queue ID before executing mutating commands, and require explicit user approval before an agent runs them. <br>


## Reference(s): <br>
- [solo-cli help man page](references/help-man-page.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that read SOLO.ro account data or mutate documents; mutating commands should require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
