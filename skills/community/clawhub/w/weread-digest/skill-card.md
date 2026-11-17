## Description:

AI-powered reading note digestion for WeRead that turns local highlights and notes into reading stats, periodic digests, book summaries, cross-book themes, and knowledge-base archive drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ben61405](https://clawhub.ai/user/ben61405)

### License/Terms of Use:

MIT-0

## Use Case:

Readers and knowledge-management users use this skill to analyze locally exported WeRead highlights and notes, generate reading reports and book summaries, and prepare confirmed Markdown archive entries for an Obsidian or plain Markdown knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Archive mode can create or update local knowledge-base files in a configured Obsidian or Markdown folder.

Mitigation: Verify the configured knowledge-base path and review the proposed file changes before confirming archive operations.

Risk: The skill depends on a separate weread skill for exported reading data and Cookie setup.

Mitigation: Install and trust the companion weread skill before use, and rerun or refresh its export flow when local data is missing or stale.

## Reference(s):

- [Weread Digest on ClawHub](https://clawhub.ai/ben61405/skills/weread-digest)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and tables, shell command snippets, JSON configuration examples, and proposed Markdown knowledge-base file changes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses locally exported WeRead data; knowledge-base archive writes are gated by configuration and explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
