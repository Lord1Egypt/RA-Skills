## Description:

reddi.tech fork of git-summary. Get a quick summary of the current Git repository including status, recent commits, branches, and contributors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect a Git repository's current state, recent commit history, branches, remotes, uncommitted changes, and contributor summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository summaries may expose sensitive remote URLs, branch names, commit messages, or contributor names.

Mitigation: Review generated summaries before sharing and ask the agent to redact remotes or private identifiers when needed.

Risk: The skill inspects local Git metadata in the current repository.

Mitigation: Use it only in repositories whose metadata you intend the agent to inspect; the security summary describes its local Git summary commands as read-only.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nissan/skills/reddi-git-summary)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown repository summary with Git command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local git command access; outbound network behavior is disabled unless the user initiates remote operations.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
