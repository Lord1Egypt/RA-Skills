## Description:

twitter-cli helps agents read Twitter/X timelines, bookmarks, searches, tweet details, and user profiles, and can also perform authenticated account actions such as posting, deleting, liking, retweeting, bookmarking, following, and unfollowing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackwener](https://clawhub.ai/user/jackwener)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to automate Twitter/X reading, search, profile lookup, and account-management workflows from a terminal-oriented interface. It is best suited for cases where the user intentionally grants account credentials and reviews write actions before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can obtain or request live Twitter/X session cookies.

Mitigation: Treat cookies as secrets, do not paste full cookie strings into chat or shared logs, and prefer local explicit credential setup.

Risk: Authenticated commands can change account state, including posting, deleting, liking, retweeting, bookmarking, following, and unfollowing.

Mitigation: Require explicit user review before any write action and use only an account the user is comfortable delegating to the agent.

Risk: Runtime browser-cookie extraction may expose high-trust browser profiles to unnecessary account-control risk.

Mitigation: Avoid browser-cookie extraction from high-trust profiles and use a dedicated browser profile or environment variables where appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackwener/skills/twitter-cli)
- [Structured Output Schema](SCHEMA.md)
- [PyPI package page](https://pypi.org/project/twitter-cli/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and YAML or JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Machine-readable command output uses a shared envelope with ok, schema_version, data, or error fields; compact mode reduces tweet fields for lower-token agent context.]

## Skill Version(s):

0.5.1 (source: server release evidence and pyproject.toml; SKILL.md frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
