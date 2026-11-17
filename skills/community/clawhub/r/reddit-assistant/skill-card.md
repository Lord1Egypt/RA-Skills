## Description:

Reddit content creation assistant for indie developers and product builders that drafts posts, researches communities, and tracks performance data via the Reddit API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edisonchenai](https://clawhub.ai/user/edisonchenai)

### License/Terms of Use:


## Use Case:

External developers, founders, and product builders use this skill to draft Reddit posts, research target subreddits, log published posts, and generate performance reports from Reddit activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports unresolved shell scripts and Bash command interpolation that could execute unintended commands.

Mitigation: Audit all referenced scripts before installation and invoke commands without shell interpolation of user-controlled content.

Risk: The skill may save local product data, subreddit profiles, drafts, post logs, and analytics reports.

Mitigation: Warn users before writing local files and review saved memory files for sensitive product or campaign information.

## Reference(s):

- [Reddit Assistant on ClawHub](https://clawhub.ai/edisonchenai/skills/reddit-assistant)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and saved local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save drafts, product configuration, subreddit profiles, post logs, and performance reports when the referenced scripts are present.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
