## Description:

Swift linting and style enforcement via the SwiftLint CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexissan](https://clawhub.ai/user/alexissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to lint Swift projects, configure SwiftLint rules, run autocorrect, and integrate style checks with Xcode or CI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SwiftLint autocorrect commands such as swiftlint --fix can modify source files.

Mitigation: Lint before autocorrecting, review the resulting git diff, and report any remaining non-autocorrectable violations separately.

Risk: Workflow examples using git stash, branch checkout, or sudo xcode-select can affect local repository or developer tool state.

Mitigation: Confirm intent before running state-changing git or system tool-selection commands, and prefer read-only linting commands when the user only asks for analysis.

## Reference(s):

- [ClawHub Swiftlint skill page](https://clawhub.ai/alexissan/skills/swiftlint)
- [SwiftLint upstream repository](https://github.com/realm/SwiftLint)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell, YAML, Swift, and CI configuration code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can propose SwiftLint commands that produce human-readable, JSON, CSV, XML, plist, SonarQube, Markdown, HTML, or JUnit reports; autocorrect commands can modify source files.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
