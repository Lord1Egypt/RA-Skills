## Description:

Fetch and analyze Hacker News content, including top stories, technical discussions, AI and programming topics, user information, comments, and trending analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiakai](https://clawhub.ai/user/qiakai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and technical analysts use this skill to retrieve Hacker News stories and user data, filter technology discussions, and generate concise briefings or JSON-backed analyses through x-cmd commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires sourcing the local x-cmd initialization script before running Hacker News commands.

Mitigation: Install and use the x-cmd dependency only from a trusted source, and review the local initialization script before sourcing it in a shell session.

## Reference(s):

- [x-cmd Hacker News module](https://www.x-cmd.com/mod/hn)
- [x-cmd agent usage index](https://www.x-cmd.com/llms.txt)
- [ClawHub skill page](https://clawhub.ai/qiakai/skills/x-hn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or process Hacker News JSON output; requires a trusted x-cmd installation and local x-cmd initialization before commands run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
