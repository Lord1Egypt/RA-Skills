## Description:

Routes saved information to monday.com, local files, or MEMORY.md based on content type and persistence needs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to decide where research, documents, operational state, credentials, and long-term memory should be saved. It is intended to reduce local clutter while keeping owner-facing content accessible in monday.com.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes loading local context by sourcing a .context file, which the security evidence flags as unsafe local configuration loading.

Mitigation: Replace shell sourcing with a safe configuration parser before use, and review any local context values before they influence storage actions.

Risk: The skill can influence whether content is sent to monday.com, stored in GitHub-backed memory, or kept in local files.

Mitigation: Require explicit confirmation before persisting or sending content outside the current workspace, especially for credentials, configuration, private conversation context, and owner-facing documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/netanel-abergel/skills/storage-router)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with tables, rules, and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs routing decisions for where an agent should save or persist information.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
