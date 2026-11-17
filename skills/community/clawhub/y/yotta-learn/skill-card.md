## Description:

A cross-agent knowledge-base skill that captures reusable methods and lessons as reviewed, searchable entries and retrieves them for later sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users and developers use it to capture validated cross-project methods, pitfalls, and tutorials in a categorized knowledge base, then retrieve verified entries before work. It guides first-time setup and directs sensitive or project-specific information elsewhere.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive information can remain in the shared local knowledge base and may be reused across agents or projects.

Mitigation: Keep secrets, personal information, and local-only details out of the shared knowledge base; sanitize and independently review entries before sharing, since draft or verified labels do not ensure confidentiality.

Risk: First-use setup changes persistent agent instructions and MCP settings, and actual host permission enforcement has not been verified.

Mitigation: Review and approve global memory and MCP changes separately, record how to undo them, and verify effective permissions in the host environment.

Risk: Installation or migration can affect the skill setup or stored knowledge.

Mitigation: Pin installation to a reviewed release and back up the knowledge base before migration.

## Reference(s):

- [Project homepage](https://github.com/YottaMeta/yotta-learn)
- [Knowledge base guide](references/kb.md)
- [FAQ](references/faq.md)
- [Usage walkthroughs](references/walkthroughs.md)
- [npm package](https://www.npmjs.com/package/@yottameta/yotta-learn)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Knowledge-base entries in Markdown, plus shell commands and agent configuration examples when setting up or using the skill.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Entries follow a draft and review workflow; verified entries are searchable across sessions and agents.]

## Skill Version(s):

0.6.6 (source: server-resolved release, frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
