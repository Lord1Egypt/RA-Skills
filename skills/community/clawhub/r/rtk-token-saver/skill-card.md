## Description:

Use rtk to reduce token usage from common shell, git, search, file-reading, test, build, and lint commands while preserving raw-output fallbacks when exact output is required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarezoe](https://clawhub.ai/user/clarezoe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose compact RTK-wrapped shell commands for repository inspection, search, git operations, tests, builds, linting, logs, and related CLI workflows. It also guides when to fall back to native commands for exact output or sensitive operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local rtk CLI may be untrusted or unsuitable for commands involving credentials or high-impact systems.

Mitigation: Verify the local rtk CLI before relying on it, and use native commands when handling secrets or when exact output is required.

Risk: Compact command output may omit details needed for a correct decision.

Mitigation: Rerun the smallest relevant native command when RTK output is insufficient for validation or debugging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clarezoe/skills/rtk-token-saver)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend native-command fallbacks when exact output, complete structured data, or secret handling is required.]

## Skill Version(s):

1.0.2 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
