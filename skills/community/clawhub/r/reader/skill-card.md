## Description:

Local-first reading and distillation engine for documents and pasted text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[projectsnowwork](https://clawhub.ai/user/projectsnowwork)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users use Reader to read local text-like files or pasted text, summarize documents, extract key points and action items, and compare drafts or reports without external sync or credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Summaries, briefs, and comparisons can leave a local history record containing filenames or paths and timestamps.

Mitigation: Avoid using the skill on highly sensitive documents if retaining that metadata locally is unacceptable.

## Reference(s):

- [Reader Philosophy](references/philosophy.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and plain text summaries, briefs, comparisons, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-first outputs; summary, brief, and comparison workflows may record local history with filenames or paths and timestamps.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
