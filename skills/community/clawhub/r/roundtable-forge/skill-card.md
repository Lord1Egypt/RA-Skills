## Description:

Roundtable Forge routes questions into structured, multi-agent, cross-disciplinary roundtable discussions using real, historical, or fictional character perspectives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fxbin](https://clawhub.ai/user/fxbin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convene structured multi-perspective discussions, select character roles, maintain shared Memory, and render outputs such as minutes, podcast scripts, and argument graphs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Roundtable prompts and Memory files may contain sensitive private data that persists in local artifacts.

Mitigation: Avoid entering sensitive private data, review Memory JSON before sharing it, and remove local artifacts that are no longer needed.

Risk: Rendered character dialogue can be mistaken for the real views of named people or fictional characters.

Mitigation: Keep the required AI-simulation disclaimer in outputs and avoid presenting generated statements as official positions.

Risk: The skill defaults to Chinese-oriented wording in some protocols and outputs.

Mitigation: Explicitly request another language or adapt the templates before using the skill in a different language context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fxbin/skills/roundtable-forge)
- [Server-resolved GitHub provenance](https://github.com/fxbin/skills/tree/main/roundtable-forge)
- [Roundtable protocol](references/roundtable-protocol.md)
- [Memory schema](references/memory-schema.md)
- [Multi-agent runtime protocol](references/multi-agent-runtime-protocol.md)
- [Output template contract](references/output-template-contract.md)
- [Sources and citations protocol](references/sources-and-citations.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and JSON-backed local artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured transcripts, shared Memory files, optional podcast scripts, and argument graph artifacts.]

## Skill Version(s):

0.1.0 (source: server release metadata); artifact VERSION reports v2.9.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
