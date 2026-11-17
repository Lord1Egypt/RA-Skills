## Description:

Self Learning Skill helps an agent analyze recent conversation history, extract durable memory and correction signals, and update persistent memory, configuration, and learning-log files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acczdy](https://clawhub.ai/user/acczdy)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to keep agent memory, identity, tool notes, workflow guidance, and learning records current after conversations, corrections, errors, and feature requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recent conversations and memory files may contain sensitive data that should not become persistent memory.

Mitigation: Avoid storing secrets in conversations or memory files, restrict the configured workspace, and review proposed updates before accepting them.

Risk: AI-generated analysis can introduce incorrect, unwanted, or misleading changes into persistent agent behavior files.

Mitigation: Run dry-run first, review generated diffs manually, and keep backup and validation controls enabled.

Risk: Broad file-writing behavior can affect more files than intended if workspace scope or filenames are not tightly controlled.

Mitigation: Prefer a patched version that enforces filename allowlists, path containment, schema validation, redaction, delete limits, and real rollback.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/acczdy/skills/self-learning)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, YAML configuration, shell commands, and CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write persistent memory and learning-log files in the configured workspace.]

## Skill Version(s):

3.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
