## Description:

Complete reference for the shared memory architecture connecting Claude Code, OpenClaw/Kimi, and LM Studio subagents through an Obsidian vault and MemPalace (ChromaDB).

This skill is ready for commercial/non-commercial use.

## Publisher:

[nerua1](https://clawhub.ai/user/nerua1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to understand and operate a local shared-memory stack for multi-agent workflows, including vault layout, MemPalace mining/search, idea capture, and Claude Code to OpenClaw communication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent shared storage and semantic indexing can retain private, regulated, or secret session content.

Mitigation: Use the skill only with content intended to be persisted in the shared vault and semantic index, and review storage scope before installation.

Risk: The documented publishing workflow and named SSH/gh credentials could enable unintended public pushes if executed by an agent.

Mitigation: Require explicit human review of repository contents and exact publishing commands before allowing any agent to use those credentials or push publicly.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nerua1/skills/shared-memory-stack)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with command examples, path references, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No standalone files are produced by the skill; it guides agents in using an existing shared-memory setup.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
