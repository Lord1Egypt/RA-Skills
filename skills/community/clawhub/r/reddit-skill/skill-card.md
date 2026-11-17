## Description:

Use ThreadPilot to manage Reddit account workflows from the CLI with human-in-the-loop safety and explicit confirmation before engagement actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vood](https://clawhub.ai/user/vood)

### License/Terms of Use:


## Use Case:

External operators and developers use this skill to verify Reddit sessions, retrieve subreddit rules, inspect account activity, and run CLI-based Reddit read, search, and engagement workflows with user confirmation before posting or liking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags unaudited external executable bootstrapping for a CLI that can access Reddit sessions or tokens.

Mitigation: Review the upstream ThreadPilot source before installing; prefer pinned immutable releases or commits and verify checksums or signatures before execution.

Risk: The skill can perform Reddit account actions such as posting, commenting, liking, and subscribing.

Mitigation: Use dry-run previews and explicit confirmation gates before engagement actions, keep duplicate-comment protection enabled, and review subreddit rules before publishing.

Risk: The security summary reports missing wrapper files for actions that can use account sessions and post or like content.

Mitigation: Review the installed launcher and wrapper contents before use and limit credentials or browser profiles to the minimum account scope needed.

## Reference(s):

- [ClawHub Reddit Skill page](https://clawhub.ai/vood/skills/reddit-skill)
- [ThreadPilot Binary Reference](bin/REFERENCE.md)
- [ThreadPilot CLI and library](https://github.com/vood/threadpilot)
- [ThreadPilot releases](https://github.com/vood/threadpilot/releases)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and environment variables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Human confirmation or dry-run preview is expected before likes and posts.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
