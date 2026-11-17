## Description:

Save conversations to a local memory index with FTS5 rebuilds, log cross-references, and saved conversation dispatch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirza42](https://clawhub.ai/user/mirza42)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to persist conversation summaries as local Markdown files, keep a human-readable conversation log, and rebuild a searchable FTS5 memory index.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist conversation summaries and index workspace Markdown, which may include sensitive local content.

Mitigation: Use it only for conversations intended for long-term local memory, avoid saving secrets, and restrict the workspace or saved-conversation directory to approved content.

Risk: Files marked off the record may still be indexed during a later rebuild.

Mitigation: Do not rely on off-the-record saves for privacy; delete sensitive saved files and rebuild or remove generated indexes before reuse.

## Reference(s):

- [Save skill page](https://clawhub.ai/mirza42/skills/save)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown summaries, local files, and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local filesystem storage and a Python stdlib FTS5 index; no external API keys are required.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
