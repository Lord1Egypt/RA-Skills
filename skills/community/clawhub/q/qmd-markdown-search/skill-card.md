## Description:

Local hybrid search for markdown notes and docs. Use when searching notes, finding related content, or retrieving documents from indexed collections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emcmillan80](https://clawhub.ai/user/emcmillan80)

### License/Terms of Use:


## Use Case:

Developers, knowledge workers, and agents use this skill to search local Markdown notes, documentation, and knowledge bases with keyword, semantic, or hybrid retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install command fetches qmd through a Bun global install path from the upstream repository.

Mitigation: Install only after reviewing the qmd upstream source or a pinned release, avoid sudo, and use a reviewed Bun global install path.

Risk: The tool indexes local Markdown folders and can expose searchable content from any collection the user adds.

Mitigation: Index only Markdown folders that are intentionally approved for search in the agent environment.

## Reference(s):

- [QMD upstream repository](https://github.com/tobi/qmd)
- [ClawHub skill page](https://clawhub.ai/emcmillan80/skills/qmd-markdown-search)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and command output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search commands may return text, file paths, full Markdown documents, or JSON when qmd is invoked with JSON options.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
