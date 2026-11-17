## Description:

Bootstrap and maintain a personal LLM wiki: a persistent, compounding knowledge base of interlinked Markdown pages that an agent writes and maintains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brunovu20](https://clawhub.ai/user/brunovu20)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to bootstrap, ingest into, query, and audit a local Markdown wiki that compounds knowledge across sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create or update multiple files under the chosen wiki directory.

Mitigation: Keep the wiki root clear, review the directory layout, and confirm ambiguous requests before allowing batch writes.

Risk: Wiki pages may contain stale, contradictory, or insufficiently sourced claims if sources change or conflict.

Mitigation: Use the skill's audit workflow to check contradictions, stale claims, missing citations, and gaps before relying on the wiki.

## Reference(s):

- [qmd](https://github.com/tobi/qmd)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, plain text, tables, shell commands, and optional code snippets depending on the request]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local wiki files under a user-selected root and keeps raw source files immutable.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
