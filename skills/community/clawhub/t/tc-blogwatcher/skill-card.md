## Description:

Monitor blogs and RSS feeds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to monitor blogs and RSS feeds, assess the user's request, and return helpful updates or guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is lightly documented and may fetch feeds or web pages and write files when the agent is asked to perform broad monitoring tasks.

Mitigation: Confirm the feeds, web pages, and files involved before execution, and review any proposed file writes or shell commands.

## Reference(s):

- [Blog Watcher ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/tc-blogwatcher)
- [terrycarter1985 ClawHub publisher profile](https://clawhub.ai/user/terrycarter1985)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on agent web fetch, web search, file read, file write, and shell tools depending on the user's monitoring task.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
