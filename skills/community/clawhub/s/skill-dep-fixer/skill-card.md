## Description:

Generates a Node.js CLI tool that scans installed OpenClaw skills for missing npm, pip, Homebrew, and system dependencies and optionally fixes supported packages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christianteohx](https://clawhub.ai/user/christianteohx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate a CLI that checks OpenClaw skill dependency declarations, reports missing tools, and installs fixable npm, pip, or Homebrew dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated workflow can install global packages or an unverified latest-release binary.

Mitigation: Use dry-run first, inspect each proposed package, avoid elevated privileges, and prefer pinned or verified installation methods.

Risk: Dependency fixes may be based on declarations from skills that have not been reviewed.

Mitigation: Install only dependencies declared by trusted skills and review the skill before installing or running fixes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/christianteohx/skills/skill-dep-fixer)
- [Project homepage](https://github.com/christianteohx/skill-dep-fixer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with JavaScript code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated CLI supports dry-run, fix, skill-specific, JSON, report, and help modes.]

## Skill Version(s):

2.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
