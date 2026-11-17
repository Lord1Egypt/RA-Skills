## Description:

Maintains an llm-wiki knowledge base by ingesting sources, answering wiki-backed questions, running health checks, and processing batch imports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiehanlin](https://clawhub.ai/user/xiehanlin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-base maintainers use this skill to keep a local llm-wiki repository organized, current, and queryable. It supports source ingestion, entity and concept updates, synthesis pages, wiki-backed answers, lint-driven maintenance, and batch imports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run a local wiki lint shell script.

Mitigation: Review the target wiki's AGENTS.md and tools/lint.sh first, and require confirmation before running lint or repair actions.

Risk: The skill relies on mutable external wiki instructions.

Mitigation: Use only a wiki directory you control and inspect its instructions before allowing writes.

Risk: Queries can lead to generated answers being saved back into the wiki.

Mitigation: Treat query workflows as potentially write-capable and require confirmation before saving generated answers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiehanlin/skills/wiki-maintainer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and wiki file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update wiki pages, logs, index entries, and lint reports when the agent is authorized to write to the target wiki.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
