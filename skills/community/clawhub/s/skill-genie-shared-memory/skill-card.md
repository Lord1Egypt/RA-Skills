## Description:

Read and write shared state for any AI agent with a dual-layer model: durable cross-agent knowledge and real-time cross-worktree runtime memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarezoe](https://clawhub.ai/user/clarezoe)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to preserve project knowledge across tools and coordinate active handoffs or runtime state across git worktrees.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent cross-agent memory can carry unreviewed or stale context across sessions, repositories, and worktrees.

Mitigation: Review memory files before agents load them and keep durable knowledge separate from runtime coordination files.

Risk: Shared and runtime memory are not appropriate for secrets or credentials.

Mitigation: Avoid storing secrets, private keys, tokens, .env content, or other credentials in shared memory layers.

Risk: Similarly named repositories may collide in private local memory paths.

Mitigation: Check the resolved project memory path before writing private local memory for repositories with similar names.

## Reference(s):

- [Shared Memory README](README.md)
- [Worktree shared framework specification](references/worktree-shared-framework.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and file path conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update memory markdown files, JSONL runtime logs, event files, and a .trellis/shared symlink when invoked by an agent.]

## Skill Version(s):

1.1.2 (source: frontmatter metadata and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
