## Description:

Local hybrid search for markdown notes and docs. Use when searching notes, finding related content, or retrieving documents from indexed collections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lifecoacher](https://clawhub.ai/user/lifecoacher)

### License/Terms of Use:


## Use Case:

Developers, knowledge workers, and agents use this skill to search and retrieve content from local Markdown note, documentation, or knowledge-base collections with qmd.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs qmd globally from an unpinned GitHub dependency through Bun.

Mitigation: Install only after trusting the upstream project, and use an isolated environment or pinned reviewed revision for higher assurance.

Risk: The skill searches local Markdown folders selected by the user.

Mitigation: Add only the specific Markdown folders intended to be searchable.

Risk: Scheduled update or embedding jobs can repeatedly process local collections.

Mitigation: Review scheduled update and embed jobs before enabling them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lifecoacher/skills/qmd-skill-2)
- [Publisher profile: lifecoacher](https://clawhub.ai/user/lifecoacher)
- [qmd upstream project](https://github.com/tobi/qmd)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes qmd install, setup, search, retrieval, indexing, and maintenance command guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
