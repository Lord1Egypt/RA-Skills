## Description:

Automates Yuque document and knowledge-base workflows through the Yuque Open API, including document CRUD, TOC management, Markdown formatting, search, and batch import/export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[feixuelingcloud](https://clawhub.ai/user/feixuelingcloud)

### License/Terms of Use:

MIT

## Use Case:

Developers and knowledge-base maintainers use this skill to operate Yuque workspaces from an agent, including publishing Markdown, reorganizing document tables of contents, searching content, and running batch import or export tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Yuque account-level document access can expose tokens or private content.

Mitigation: Use a least-privilege Yuque token and keep the default official API URL unless a private deployment is trusted.

Risk: Batch, TOC, delete, import, replace, or raw API operations can unintentionally modify or remove Yuque content.

Mitigation: Back up important repositories and require explicit user approval before these actions.

Risk: The server security verdict is suspicious because the skill combines document automation with unsafe defaults.

Mitigation: Review the skill carefully before installing and scan it before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/feixuelingcloud/skills/yuque-skill)
- [Yuque API Reference](references/api_reference.md)
- [Yuque Markdown Format Guide](references/markdown_format.md)
- [Yuque TOC Operations Guide](references/toc_operations.md)
- [Official Yuque Developer API](https://www.yuque.com/yuque/developer/api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled scripts return JSON to stdout for agent post-processing and user-facing summaries.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
