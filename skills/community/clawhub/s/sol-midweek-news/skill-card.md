## Description:

Midweek AI digest - Wednesday briefing of the 3 most significant AI stories from the past 3 days, in Sol's voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amrree](https://clawhub.ai/user/amrree)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to automate a weekly AI-news briefing workflow that selects recent AI/ML stories, writes concise commentary, and publishes a Jekyll blog post.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run as scheduled local automation and publish GitHub changes without manual approval.

Mitigation: Enable a dry-run or review step before commit and push, and require explicit confirmation for publication.

Risk: The workflow reads a local MiniMax API key and edits a specific Jekyll repository path.

Mitigation: Document secret handling, scope repository access narrowly, and verify the target path before enabling the schedule.

Risk: Launchd scheduling may keep the automation active after initial setup.

Mitigation: Provide clear install, status, and removal instructions for the launchd job.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amrree/skills/sol-midweek-news)
- [Publisher profile](https://clawhub.ai/user/amrree)
- [Skill-body source link: sol-skills-bundle](https://github.com/TheSolAI/sol-skills-bundle)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown Jekyll post with local file changes and git commit/push actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a MiniMax API key, a configured local Jekyll repository, and a Wednesday 8am UK launchd schedule.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
