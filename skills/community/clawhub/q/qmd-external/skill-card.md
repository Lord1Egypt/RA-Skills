## Description:

Local hybrid search for markdown notes and docs. Use when searching notes, finding related content, or retrieving documents from indexed collections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[levineam](https://clawhub.ai/user/levineam)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to search local Markdown notes, documentation, and knowledge bases, retrieve matching documents, and keep indexed collections current.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing qmd directly from its upstream repository can introduce supply-chain risk.

Mitigation: Review the upstream repository before installation and pin the install to a known commit or release when possible.

Risk: The skill indexes local Markdown folders and may expose content from collections the user adds.

Mitigation: Only add Markdown folders intended for search and retrieval.

Risk: The optional recurring reindex job runs local indexing on a schedule.

Mitigation: Create the cron job only when recurring local indexing is desired and acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/levineam/skills/qmd-external)
- [qmd project homepage](https://github.com/tobi/qmd)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output depends on local indexed Markdown collections and qmd command options.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
