## Description:

Quad-layer memory system integration - unifies OpenClaw, Claude Code, and self-improving agent memories into a single knowledge lake.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanxiao-bot](https://clawhub.ai/user/hanxiao-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to maintain a local long-term memory lake that consolidates Claude Code session history, OpenClaw daily logs, self-improving agent metrics, derived patterns, domain notes, tool notes, and review records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sync scripts can duplicate private Claude Code session logs and OpenClaw agent metrics into persistent skill-local storage.

Mitigation: Run the scripts only for approved projects, review source paths before syncing, and exclude secrets, confidential sessions, or regulated data from the source directories.

Risk: Generated pattern files may summarize private or sensitive session content and may be mistaken for trusted instructions.

Mitigation: Review generated pattern files before use, treat them as untrusted memory artifacts, and remove sensitive or incorrect entries before relying on them.

Risk: The skill does not document consent, minimization, redaction, or retention controls for copied memory data.

Mitigation: Define local retention and deletion procedures before adoption, and periodically audit the memory directory for unnecessary or sensitive retained data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hanxiao-bot/skills/triple-memory-lake)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and generated local memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent local memory artifacts under the skill's memory directory; pattern mining limits copied error examples to 100 entries per run.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
