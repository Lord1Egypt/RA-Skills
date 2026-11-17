## Description:

Local hybrid search for markdown notes and docs. Use when searching notes, finding related content, or retrieving documents from indexed collections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmaeter](https://clawhub.ai/user/pmaeter)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to search, retrieve, and maintain indexed local Markdown notes, documentation, and knowledge-base collections with qmd.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install step uses a global Bun install from a third-party upstream repository.

Mitigation: Install only after reviewing and trusting the qmd upstream repository and the implications of a globally installed command-line tool.

Risk: The skill indexes local Markdown folders selected by the user.

Mitigation: Add only Markdown folders intended for search and retrieval, especially when collections may contain sensitive notes or documents.

Risk: Optional cron or scheduler setup can keep local indexes and embeddings updated over time.

Mitigation: Enable scheduled updates only as a deliberate maintenance choice and review the configured commands and paths.

## Reference(s):

- [Qmd upstream repository](https://github.com/tobi/qmd)
- [ClawHub skill page](https://clawhub.ai/pmaeter/skills/qmd-skill-main)
- [Publisher profile](https://clawhub.ai/user/pmaeter)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text, json]

**Output Format:** [Markdown guidance with inline shell commands and optional qmd JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the qmd binary; supports local Markdown collection search, retrieval, indexing, embedding, and maintenance workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
