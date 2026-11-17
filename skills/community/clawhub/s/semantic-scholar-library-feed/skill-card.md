## Description:

Work with a user's Semantic Scholar account to read Research Feeds, inspect private Library folders, add papers to folders, and resolve Semantic Scholar paper records from identifiers such as arXiv IDs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zjsxply](https://clawhub.ai/user/zjsxply)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to operate against authenticated Semantic Scholar Library and Research Feed surfaces, including feed export, private folder inspection, folder updates, and Semantic Scholar paper ID resolution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores live Semantic Scholar session cookies on disk.

Mitigation: Treat saved cookie files like passwords, keep them out of repositories, shared folders, logs, and backups, and remove or rotate them when no longer needed.

Risk: Authenticated cookies can be sent with user-supplied page URLs in feed and SSR commands.

Mitigation: Use --page-url only with https://www.semanticscholar.org until the skill constrains authenticated requests to the official origin.

Risk: Folder update commands can modify a user's private Semantic Scholar Library.

Mitigation: Resolve paper IDs, diff against current folder entries, use dry-run behavior where available, and re-fetch the folder to verify expected changes.

## Reference(s):

- [Authentication And Cookie Store](references/auth-and-cookies.md)
- [Library Workflow](references/library.md)
- [Research Feed Workflow](references/research-feed.md)
- [Semantic Scholar](https://www.semanticscholar.org)
- [Semantic Scholar Graph API](https://api.semanticscholar.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON file outputs from the bundled CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or read local cookie-store files and JSON exports when the agent runs the bundled CLI.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
