## Description:

Automatically generates sprint release notes from a GitHub Project Board, groups completed items by repository, and publishes per-repository Markdown as GitHub Release descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tenkus47](https://clawhub.ai/user/tenkus47)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to summarize completed GitHub Project Board sprint work, evaluate contributor activity, and prepare release notes for the repositories that shipped changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can publish GitHub Releases to repositories selected from project-board data.

Mitigation: Run in dry-run mode first and require an explicit preflight approval list of target repositories before publishing.

Risk: The workflow requires GitHub credentials with repository and project access.

Mitigation: Use a fine-grained GitHub token scoped only to approved repositories, and do not store the token in config files or pass it on the command line.

Risk: Contributor scoring and optional notification behavior can affect people or external channels.

Mitigation: Treat contributor scoring and notification webhooks as opt-in behavior and review generated summaries before publication.

## Reference(s):

- [Contributor Scoring & Evaluation Reference](references/contributor-scoring.md)
- [GitHub API Queries Reference](references/github-queries.md)
- [ClawHub Skill Page](https://clawhub.ai/tenkus47/skills/sprint-release-notes)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown release notes with command and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local Markdown files, publish GitHub Releases, and optionally post a summary comment when configured.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
