## Description:

Build and maintain a local Markdown-based knowledge wiki with Obsidian-style double-links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexfly123lee-creator](https://clawhub.ai/user/alexfly123lee-creator)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create and maintain a local Markdown knowledge base from research articles, competitive analysis, or domain knowledge. It supports ingest, query, lint, and maintenance workflows for Obsidian-style wiki structures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's Git workflow instructs the agent to stage the entire working tree after each operation batch, which can accidentally include unrelated files or secrets.

Mitigation: Use the skill in a dedicated wiki repository or inspect git status and staged diffs before committing; stage only intended wiki/ and outputs/ changes.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file paths, wiki page templates, shell commands, and structured maintenance instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local wiki content under wiki/ and reports under outputs/ when applied by an agent.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
