## Description:

Manage Yuque knowledge base documents and repositories, including reading documents, listing repositories, searching content, creating documents, and managing knowledge bases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a6590072](https://clawhub.ai/user/a6590072)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-base operators use this skill to interact with Yuque repositories and documents from an agent workflow. It supports personal and team spaces for document discovery, retrieval, creation, update, and deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Yuque token may grant access to important personal or team knowledge bases.

Mitigation: Set YUQUE_TOKEN through a protected environment or secret manager and grant the token the narrowest Yuque permissions available.

Risk: The skill supports create, update, and delete operations, including under-disclosed destructive document deletion capability.

Mitigation: Require explicit user confirmation before create, update, or delete operations, especially for team repositories.

Risk: Passing tokens through command-line arguments can expose credentials through shell history or process listings.

Mitigation: Prefer the YUQUE_TOKEN environment variable or a secret manager rather than the --token argument.

## Reference(s):

- [Yuque API Reference](artifact/references/api.md)
- [Yuque API Base URL](https://www.yuque.com/api/v2)
- [ClawHub Skill Page](https://clawhub.ai/a6590072/skills/yuque)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Python CLI examples, JSON API responses, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May issue authenticated Yuque API operations when used with a valid YUQUE_TOKEN.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
