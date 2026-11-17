## Description:

Swiftverify helps agents validate Swift and SwiftUI projects against Apple Design Award-oriented quality checks for build health, architecture, design-system use, accessibility, internationalization, performance, native integration, and testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soponcd](https://clawhub.ai/user/soponcd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill after feature work, before pull-request merge, or before release to run or plan Swift/SwiftUI validation checks and produce a consolidated verification report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run local build, lint, and test commands in the target repository.

Mitigation: Review the validation entrypoint before use, run it in an appropriate local or CI environment, and confirm that generated reports are handled according to the repository's artifact policy.

Risk: The documentation contains inconsistent entrypoint paths and generated report handling expectations.

Mitigation: Confirm the actual verification command and decide whether specs/verification_report.md should be committed or treated as a generated build artifact before CI adoption.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/soponcd/skills/swiftverify)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and report guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update a verification report artifact when the referenced validation flow is executed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
