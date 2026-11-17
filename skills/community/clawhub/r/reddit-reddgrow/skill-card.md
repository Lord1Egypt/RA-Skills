## Description:

Reddit intelligence CLI for AI agents that supports Reddit posts, subreddit research, comments, user profiles, wiki pages, domain mentions, marketing, community rules, and URL checking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yahavf6](https://clawhub.ai/user/yahavf6)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run ReddGrow workflows for Reddit research, community rule checks, post and comment analysis, user profile review, domain monitoring, and pre-posting checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to globally install mutable third-party npm code.

Mitigation: Install only after trusting the ReddGrow package and publisher; consider pinning or locally installing a reviewed CLI version.

Risk: The skill requires handling a ReddGrow API key.

Mitigation: Use a securely managed REDDGROW_API_KEY environment secret instead of typing the key into shell commands.

Risk: Use outside the intended Reddit research scope can increase operational and policy risk.

Mitigation: Keep the skill limited to Reddit research tasks and follow subreddit rules, duplicate-link checks, and posting restrictions before taking action.

## Reference(s):

- [ReddGrow homepage](https://reddgrow.ai)
- [ClawHub skill page](https://clawhub.ai/yahavf6/skills/reddit-reddgrow)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON-output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the reddgrow CLI and a REDDGROW_API_KEY environment secret.]

## Skill Version(s):

0.1.6 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
