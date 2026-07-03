## Description: <br>
Tencent Docs is an agent skill for creating, reading, editing, searching, importing, exporting, and managing docs.qq.com cloud documents across document, sheet, slide, mind map, flowchart, smart table, form, OCR, and web clipping workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codercuixin](https://clawhub.ai/user/codercuixin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to work with Tencent Docs on behalf of a user, including creating formatted documents, spreadsheets, slides, diagrams, and forms; searching or reading cloud documents; importing local files; clipping web pages; and running OCR workflows. It is intended for users and teams that want an agent to manage docs.qq.com content through a configured Tencent Docs token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Tencent Docs token and can manage cloud document content. <br>
Mitigation: Use a dedicated token with the minimum acceptable access, avoid connecting sensitive workspaces, and rotate the token if logs or configuration output may have exposed it. <br>
Risk: Security evidence reports silent unsupported-feature reporting and recommends avoiding sensitive prompts or documents until it is removed or made opt-in. <br>
Mitigation: Use the skill only with non-sensitive prompts and documents unless reporting behavior has been reviewed and made explicit to the user. <br>
Risk: Security evidence reports under-scoped high-impact document actions, including document management, upload, sharing, and destructive operations. <br>
Mitigation: Require explicit user confirmation before deletion, sharing changes, imports, exports, or bulk edits, and keep backups or version history available for important documents. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/codercuixin/test-my) <br>
- [Tencent Docs](https://docs.qq.com/home) <br>
- [Tencent Docs Token Authorization](https://docs.qq.com/scenario/open-claw.html?nlc=1) <br>
- [Authentication Reference](artifact/references/auth.md) <br>
- [Workflow Reference](artifact/references/workflows.md) <br>
- [Smart Canvas Reference](artifact/smartcanvas/entry.md) <br>
- [File Management Reference](artifact/references/manage_references.md) <br>
- [OCR Reference](artifact/references/ocr_references.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with JSON arguments, shell commands, and Tencent Docs URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, modify, delete, share, import, export, or read Tencent Docs content when a Tencent Docs token is configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.33) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
