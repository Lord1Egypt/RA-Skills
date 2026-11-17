## Description:

Research a topic via web search, auto-match a relevant GIF, and log results as a Bear note using a configurable template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to gather web research on a topic, add a matching GIF for context, and create a structured Bear note from a configurable template.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User or web-derived text may be handled unsafely and lead to unintended local command execution.

Mitigation: Review before installing and avoid untrusted input until template rendering uses a data-safe method and tag arguments are passed safely.

Risk: Confidential research topics may be exposed through search, GIF lookup, or note-creation dependencies.

Mitigation: Do not use the skill with confidential research topics unless the data path and dependencies have been reviewed.

Risk: The grizzly dependency may change behavior if installed without version pinning.

Mitigation: Pin grizzly to a reviewed version before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/research-logger-tool)
- [Publisher profile](https://clawhub.ai/user/terrycarter1985)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown note content and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a Bear note from search snippets, source links, tags, and GIF metadata when dependencies are available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
