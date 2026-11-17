## Description:

Interact with a Readwise Reader library to list, create, update, and delete documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xinthink](https://clawhub.ai/user/xinthink)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage saved articles and reading lists in Readwise Reader, including querying content, saving new documents, updating metadata, bulk editing items, deleting documents, and listing tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Readwise access token that can read and modify the user's Reader library.

Mitigation: Install only when that access is acceptable, keep READWISE_ACCESS_TOKEN private, and prefer an isolated environment for dependency installation.

Risk: Update, bulk update, and delete commands can change or remove Reader documents.

Mitigation: Review JSON payloads and document IDs before execution, use dry-run support where available, and avoid --confirm until the intended deletions are verified.

Risk: Dependency versions are not fully pinned in the artifact.

Mitigation: Use a virtual environment and consider pinning dependencies before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xinthink/skills/readwise-reader)
- [Usage guide](references/usage-guide.md)
- [Readwise access token page](https://readwise.io/access_token)
- [Project homepage](https://github.com/xinthink/reader-mcp-server)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON payload examples; scripts return JSON or JSON Lines.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python, pip, and READWISE_ACCESS_TOKEN; some scripts can write JSON or JSON Lines to output files.]

## Skill Version(s):

0.2.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
