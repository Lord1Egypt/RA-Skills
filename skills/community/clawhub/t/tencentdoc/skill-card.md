## Description: <br>
Tencent Docs Skill helps agents create, edit, read, manage, import, export, and share Tencent Docs documents, spreadsheets, slides, diagrams, smart sheets, forms, and knowledge-space files through Tencent Docs MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nmww](https://clawhub.ai/user/nmww) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to automate Tencent Docs workflows, including creating and editing online documents, spreadsheets, slides, diagrams, smart sheets, forms, and workspace files. It is intended for live Tencent Docs accounts after OAuth authorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad live Tencent Docs control, including reading, creating, editing, deleting, importing/exporting, and sharing documents. <br>
Mitigation: Install only for accounts where that access is acceptable, verify exact file IDs and sheet ranges before edits, and manually confirm destructive operations or public sharing changes. <br>
Risk: Authorization tokens and command output can expose sensitive Tencent Docs access. <br>
Mitigation: Protect mcporter configuration and command logs, avoid shared machines, and reauthorize or revoke access if a token may have been exposed. <br>
Risk: Import and upload workflows can send local files or scraped web content into Tencent Docs storage. <br>
Mitigation: Confirm upload paths, source URLs, destination folders, and document permissions before running import, upload, or web-scraping workflows. <br>


## Reference(s): <br>
- [ClawHub Tencent Docs Skill Page](https://clawhub.ai/nmww/tencentdoc) <br>
- [Tencent Docs Home](https://docs.qq.com/home) <br>
- [Tencent Docs Auth](artifact/references/auth.md) <br>
- [Tencent Docs Workflows](artifact/references/workflows.md) <br>
- [Tencent Docs File Management](artifact/references/manage_references.md) <br>
- [Smartcanvas Entry](artifact/smartcanvas/entry.md) <br>
- [Sheet Entry](artifact/sheet/entry.md) <br>
- [Document Entry](artifact/doc/entry.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with JSON arguments, shell commands, and Tencent Docs links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tencent Docs OAuth authorization and may create, modify, delete, import, export, or share live Tencent Docs content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.20) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
