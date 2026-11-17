## Description:

Produce a short, copy-paste-ready TL;DR summary of any CLI command from its man page or --help text, so a human or coding agent can learn the essential options without scrolling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and coding agents use this skill to get a compact reminder of a local CLI command's purpose, syntax, common flags, and an example before invoking or reviewing that command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may execute the user-supplied command with --help when no man page summary is available.

Mitigation: Use it only with trusted command names and in environments where PATH cannot be influenced by untrusted repositories or directories.

Risk: The generated summary can be incomplete or unavailable when local man pages or --help output are missing or nonstandard.

Mitigation: Treat the summary as a quick reference and confirm important flags or behavior against authoritative command documentation before high-impact use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/tldr-cmd)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text summary with command, about, usage, flags, and example sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No network access is required; output depends on local man pages and --help text availability.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
