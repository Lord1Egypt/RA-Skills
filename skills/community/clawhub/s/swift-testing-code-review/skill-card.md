## Description:

Reviews Swift Testing code for proper use of #expect/#require, parameterized tests, async testing, and organization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and code reviewers use this skill to review Swift Testing code for assertion quality, parameterized test behavior, async testing patterns, and suite organization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt an agent to inspect Swift files placed in review scope.

Mitigation: Provide an explicit review scope and exclude files that should not be reviewed.

Risk: The skill asks the agent to rely on a separate review-verification-protocol skill when available.

Mitigation: Confirm that the companion protocol is installed when strict review anchoring is required.

## Reference(s):

- [#expect Macro](references/expect-macro.md)
- [Parameterized Tests](references/parameterized.md)
- [Async Testing](references/async-testing.md)
- [Test Organization](references/organization.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown review findings and review-summary text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings should cite reviewed Swift file and line evidence when issues are reported.]

## Skill Version(s):

1.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
