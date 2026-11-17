## Description:

Tests ClawHub CLI publish behavior by documenting expected publish parameters and exposing a minimal Python test script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forealmy](https://clawhub.ai/user/forealmy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release maintainers use this skill as a publish-test fixture for checking ClawHub CLI argument handling around name, version, tags, and changelog metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation may overstate what this minimal fixture verifies.

Mitigation: Treat it as a publish-test fixture, not a complete ClawHub CLI validation suite.

Risk: Users may assume the included script performs meaningful CLI checks.

Mitigation: Review the artifact behavior before relying on it; the script only prints a simple test message.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/forealmy/skills/test-clawhub-skill)
- [Publisher profile](https://clawhub.ai/user/forealmy)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell command examples and plain text script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external tools, credentials, APIs, or network access are described by the artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
