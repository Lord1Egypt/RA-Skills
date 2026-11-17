## Description:

Smith Matrix guides agents in building a recursive multi-agent workspace that decomposes complex tasks into bounded parallel subagents with directory-isolated coordination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyijun](https://clawhub.ai/user/cyijun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Smith Matrix to decompose complex tasks into bounded parallel subagents, coordinate them through inbox/outbox files, and aggregate results without cross-agent write conflicts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and retains a .smith-matrix directory containing task descriptions, outputs, and private agent notes.

Mitigation: Avoid placing secrets or sensitive data in tasks, and review generated files before committing or sharing them.

Risk: Recursive task decomposition can create unnecessary child work when the task scope is too broad or vague.

Mitigation: Use the documented maximum depth and child-agent limits, and require each parent agent to summarize results and stop at terminal depth.

## Reference(s):

- [Smith Matrix ClawHub release](https://clawhub.ai/cyijun/skills/smith-matrix)
- [Core Concepts](references/concepts.md)
- [Protocol Specification](references/protocol.md)
- [Best Practices](references/best-practices.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with workspace file instructions and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a .smith-matrix workspace tree with task, private, outbox, and result files when used.]

## Skill Version(s):

0.1.3 (source: server release metadata; artifact frontmatter lists 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
