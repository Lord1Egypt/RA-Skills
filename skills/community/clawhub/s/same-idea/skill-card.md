## Description:

Finds similar ideas, resonating quotes, and related concepts in a user's Logseq and Obsidian reading notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:


## Use Case:

External users and knowledge workers use this skill to compare a new thought, concept, or quote against their personal reading notes and discover related excerpts with source context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill searches personal Logseq and Obsidian vaults and may return private note excerpts.

Mitigation: Install and run it only when agent access to those note vaults is acceptable, and review excerpts before sharing them outside the workspace.

Risk: The bundled release script can stage local files, create commits and tags, and push to a GitHub remote.

Mitigation: Do not run scripts/release.sh during normal use; maintainers should review the repository, remote, and staged files before using it.

Risk: Keyword-based matching can miss relevant ideas or over-rank weak textual matches.

Mitigation: Treat returned matches as suggestions and verify the surrounding source context before relying on them.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style match summaries supported by JSON search results from local note searches]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Searches local Logseq and Obsidian vaults, ranks matching excerpts, and includes source attribution when available.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
