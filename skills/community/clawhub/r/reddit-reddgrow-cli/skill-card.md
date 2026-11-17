## Description:

Reddit intelligence CLI for AI agents. Use when working with reddit posts, subreddit research, comments, user profiles, wiki pages, domain mentions, marketing, community rules, or URL checking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yahavf6](https://clawhub.ai/user/yahavf6)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to research Reddit communities, posts, comments, users, domain mentions, subreddit rules, and wiki guidance through the ReddGrow CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unpinned global CLI can change behavior across installations.

Mitigation: Pin a reviewed @reddgrow/cli version or run the CLI in a sandbox before use.

Risk: Passing the ReddGrow API key in command arguments or chats can expose credentials.

Mitigation: Prefer REDDGROW_API_KEY in a protected environment and use a narrowly scoped key.

## Reference(s):

- [ReddGrow homepage](https://reddgrow.ai)
- [ClawHub skill page](https://clawhub.ai/yahavf6/skills/reddit-reddgrow-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands; ReddGrow CLI commands output JSON to stdout.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the reddgrow binary and REDDGROW_API_KEY for authenticated CLI use.]

## Skill Version(s):

0.1.7 (source: server release metadata; artifact frontmatter reports 0.1.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
