## Description:

Compress conversation context into a TurboQuant vector store inside OpenClaw memory, then retrieve the most relevant entries on demand to stay within token budgets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twacqwq](https://clawhub.ai/user/twacqwq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to persist compressed conversation context, retrieve relevant prior entries within a token budget, and compact the memory store over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent conversation memory can retain secrets, personal data, or other sensitive text across restarts.

Mitigation: Use only with redaction, deletion controls, retention limits, and clear guidance to avoid storing sensitive conversations.

Risk: Retrieved prior messages reused as system-prompt context can introduce stale, misleading, or untrusted content into later agent behavior.

Mitigation: Treat retrieved memory as contextual evidence rather than instructions, separate trust boundaries, and review or filter entries before including them in privileged prompts.

Risk: Dependency and environment setup may be hard to audit if the runtime dependencies are not pinned and reviewed.

Mitigation: Install from an auditable project checkout, pin dependencies, and review the uv environment before deployment.

## Reference(s):

- [OpenClaw TurboQuant repository](https://github.com/openclaw/openclaw-turboquant)
- [ClawHub skill page](https://clawhub.ai/twacqwq/skills/turboquant)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash command examples and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv on PATH, caller-provided embedding vectors, and a project environment initialized with uv sync.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
