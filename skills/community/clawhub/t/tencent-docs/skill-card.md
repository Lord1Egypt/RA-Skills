## Description:

Tencent Docs lets agents create, read, edit, manage, import, export, and organize docs.qq.com documents, spreadsheets, slides, diagrams, smart tables, forms, and knowledge-space files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyang58](https://clawhub.ai/user/liyang58)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to operate Tencent Docs cloud documents from an agent workflow, including creating, editing, reading, searching, importing, exporting, and organizing online documents and workspace files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent Tencent Docs authorization can grant ongoing document access through mcporter configuration.

Mitigation: Install only after review, store tokens in an approved secret location, and revoke or rotate the token when access is no longer required.

Risk: The skill can edit, delete, move, export, import, and change permissions for Tencent Docs files.

Mitigation: Require explicit user confirmation for destructive actions, permission changes, exports, imports, and operations on broadly shared documents.

Risk: Local files, web clips, and prompt-derived content may be uploaded to Tencent services.

Mitigation: Avoid sensitive or regulated content unless the user has approved the upload destination and data-handling requirements.

Risk: Unsupported-feature reporting may silently send prompt context or unmet requests.

Mitigation: Remove or disable silent reporting before use with confidential prompts or environments requiring explicit telemetry consent.

Risk: Setup and update paths can install global npm packages and follow remote update instructions.

Mitigation: Review setup commands and remote update instructions before execution, and pin or verify dependencies in managed environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liyang58/skills/tencent-docs)
- [Tencent Docs Home](https://docs.qq.com/home)
- [Tencent Docs Token Setup](https://docs.qq.com/scenario/open-claw.html?nlc=1)
- [Authentication Reference](references/auth.md)
- [Common Workflows](references/workflows.md)
- [Smartcanvas Entry](smartcanvas/entry.md)
- [Sheet Entry](sheet/entry.md)
- [Document Engine Reference](references/docengine_references.md)
- [Slide Reference](references/slide_references.md)
- [Smartsheet Reference](references/smartsheet_references.md)
- [Space Management Reference](references/space_references.md)
- [File Management Reference](references/manage_references.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON arguments, shell commands, and generated Tencent Docs links or identifiers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke Tencent Docs MCP tools, local helper scripts, and asynchronous polling workflows.]

## Skill Version(s):

1.0.31 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
