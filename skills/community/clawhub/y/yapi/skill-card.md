## Description:

Query and sync YApi interface documentation. Use when user mentions Yapi interface docs, asks for request/response details, or needs docs sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leeguooooo](https://clawhub.ai/user/leeguooooo)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to query YApi interface documentation, inspect request and response details, and sync local documentation with YApi projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run an unpinned npm fallback that may execute changing third-party code while handling YApi authentication and local project files.

Mitigation: Prefer a preinstalled or pinned, reviewed yapi/@leeguoo/yapi-mcp version and avoid the unpinned npx fallback in sensitive environments.

Risk: Documentation sync can make real changes to YApi project documentation and may use local configuration or cached authentication.

Mitigation: Confirm the target base URL, project, category, and authentication context, then run docs sync with --dry-run before a real sync.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include YApi CLI commands, URL and project/category resolution steps, and dry-run guidance before documentation sync.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
