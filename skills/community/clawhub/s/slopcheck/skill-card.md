## Description:

Validate npm package references in markdown, YAML, and config files against the live npm registry before installing or using them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mattschaller](https://clawhub.ai/user/mattschaller)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to scan AI-generated documentation, configuration, and repository files for npm package references before installing or committing them. It helps identify package names that are missing from npm or held by the registry for security reasons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The primary examples run an unpinned npm CLI through npx, which can execute package code that was not part of the reviewed artifact.

Mitigation: Prefer a pinned and reviewed package version such as slopcheck@0.1.2 and run it in a constrained environment without unrelated secrets.

Risk: The skill validates package existence and registry security holds, but it does not determine whether an existing npm package is safe, compatible, or correctly versioned.

Mitigation: Use dependency security and compatibility tools for package.json, lock files, malicious-package review, and version validation before installation or deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mattschaller/skills/slopcheck)
- [slopcheck documentation](https://github.com/mattschaller/slopcheck)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON scan output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports package existence results, security holds, source file locations, and exit-code interpretation.]

## Skill Version(s):

0.1.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
