## Description: <br>
WizNote is a connector for WizNote account automation, including note search, reading, creation, updates, deletion, attachment handling, categories, tags, comments, and sharing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangfengxiang](https://clawhub.ai/user/wangfengxiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to connect an MCP-compatible agent to a WizNote account for searching, reading, creating, modifying, sharing, and exporting notes and attachments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation includes example WizNote account credentials. <br>
Mitigation: Replace examples with safely stored secrets before use, and rotate any exposed password if it was real. <br>
Risk: The skill can modify WizNote content through create, update, delete, move, copy, category, tag, comment, share, and attachment operations. <br>
Mitigation: Use only with a trusted publisher and account scope, and explicitly confirm destructive or sharing actions before execution. <br>
Risk: The skill can fetch URL content, connect to a configured WizNote server, and download attachments or resources. <br>
Mitigation: Restrict configuration and URL-import workflows to trusted HTTPS endpoints and review attachment-download requests before running them. <br>
Risk: Downloaded notes, attachments, OCR text, and extracted document text may contain sensitive account data. <br>
Mitigation: Store local outputs in an approved workspace, limit extraction size when possible, and remove exported files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub WizNote release page](https://clawhub.ai/wangfengxiang/wiznote) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, API Calls] <br>
**Output Format:** [JSON tool responses with note content, Markdown, Base64 attachments, and optional saved local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May download note resources and attachments into local output directories when requested.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
