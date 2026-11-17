## Description:

Fetches and analyzes Hacker News content for top stories, technical discussions, AI and machine learning topics, programming, software engineering, startups, user information, comments, and trend briefings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiakai](https://clawhub.ai/user/qiakai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, software engineers, AI researchers, and agents use this skill to retrieve Hacker News story lists, post details, comments, and user information, then filter or summarize them for technology briefings and topic analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires sourcing an unpinned external shell initialization file with the agent's privileges.

Mitigation: Use only when the x-cmd installation source is trusted, and prefer running it in a constrained environment without unrelated credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiakai/skills/x-hacker-news)
- [x-cmd Hacker News module](https://www.x-cmd.com/mod/hn)
- [x-cmd agent entrypoint](https://www.x-cmd.com/llms.txt)

## Skill Output:

**Output Type(s):** [shell commands, configuration, json, text, markdown, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON or plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses x-cmd commands and may rely on cached Hacker News data.]

## Skill Version(s):

1.0.4 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
