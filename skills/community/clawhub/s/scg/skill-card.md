## Description:

Generates tailored context windows with relevant code patterns, pitfalls, StackOverflow results, and local project context for AI coding tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[captainsvbot](https://clawhub.ai/user/captainsvbot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to generate concise, task-specific context for AI coding agents. It combines goal parsing, local project search, built-in coding patterns, and optional StackOverflow search into a bounded Markdown context window.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task wording can be sent to StackOverflow through the web search path.

Mitigation: Use --no-web for private, proprietary, or sensitive tasks.

Risk: Local indexing can read source, Markdown, and JSON files from paths provided by the user, which may surface secrets or proprietary content.

Mitigation: Pass the narrowest useful --context path and avoid indexing folders that may contain secrets or material that should not enter an agent context.

Risk: Generated context may include external or local guidance that is incomplete, outdated, or not appropriate for the target codebase.

Mitigation: Review the generated context before handing it to an autonomous coding agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/captainsvbot/skills/scg)
- [Publisher profile](https://clawhub.ai/user/captainsvbot)
- [StackExchange advanced search API endpoint](https://api.stackexchange.com/2.3/search/advanced)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown context window with headings, links, file excerpts, and fenced code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Respects a configurable token budget and may include local file excerpts and StackOverflow links.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
