## Description:

Local hybrid search for markdown notes and docs. Use when searching notes, finding related content, or retrieving documents from indexed collections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aryannate](https://clawhub.ai/user/aryannate)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to search local Markdown notes, documentation, and knowledge-base collections, then retrieve matching files or document content for follow-up work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install path globally installs qmd from its current GitHub source via Bun without a pinned commit or release.

Mitigation: Install only after reviewing the referenced source, and prefer pinning a reviewed commit or release where possible.

Risk: Indexed Markdown collections become searchable by the agent and may contain sensitive local content.

Mitigation: Add only folders intentionally approved for indexing and search.

## Reference(s):

- [qmd GitHub repository](https://github.com/tobi/qmd)
- [Qmd ClawHub skill page](https://clawhub.ai/aryannate/skills/qmd-skill-4)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include qmd command examples, setup steps, search-mode selection guidance, and JSON output options for downstream agent use.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
