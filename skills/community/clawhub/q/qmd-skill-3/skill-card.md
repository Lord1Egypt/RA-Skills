## Description:

Local hybrid search for markdown notes and docs. Use when searching notes, finding related content, or retrieving documents from indexed collections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lelo78](https://clawhub.ai/user/lelo78)

### License/Terms of Use:


## Use Case:

Developers, knowledge workers, and agent operators use this skill to search, retrieve, and maintain indexed local Markdown notes, documentation, and knowledge bases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install command globally installs qmd from a mutable GitHub source that may change after review.

Mitigation: Install only from a trusted upstream source and prefer pinning to a reviewed commit or release.

Risk: The skill can make local Markdown collections searchable and retrievable by an agent.

Mitigation: Index only Markdown collections that are intentionally approved for agent access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lelo78/skills/qmd-skill-3)
- [qmd upstream repository](https://github.com/tobi/qmd)
- [Publisher profile](https://clawhub.ai/user/lelo78)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide agents to run qmd search, retrieval, indexing, embedding, and maintenance commands against user-selected Markdown collections.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
