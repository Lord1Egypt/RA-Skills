## Description:

Monitor blogs and RSS feeds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users use this skill to monitor blogs and RSS feeds and receive help coordinating blog-watcher tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes broad command execution and file-writing capabilities without clear operating limits.

Mitigation: Require explicit confirmation before shell commands or local file writes and review proposed changes before execution.

Risk: The instructions are sparse and do not define approved blog or RSS sources or storage paths.

Mitigation: Clarify allowed sources, destinations, and storage paths before using the skill in a workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/terry-blogwatcher)
- [ClawHub publisher profile](https://clawhub.ai/user/terrycarter1985)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional code and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose web, shell, read, and write actions; users should review commands and file writes before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
