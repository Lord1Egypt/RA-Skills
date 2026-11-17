## Description:

Swift Concurrency review and remediation for Swift 6.2+. Use when asked to review Swift Concurrency usage, improve concurrency compliance, or fix Swift concurrency compiler errors in a feature or file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steipete](https://clawhub.ai/user/steipete)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to review Swift 6.2+ concurrency usage, diagnose compiler errors, and apply focused fixes for actor isolation, Sendable safety, global state, and SwiftUI concurrency patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Concurrency fixes can change actor isolation, Sendable conformance, or execution context in ways that affect app behavior.

Mitigation: Review resulting Swift code changes, especially actor-isolation and Sendable decisions, and run the project's compiler and tests before deployment.

Risk: The skill may guide an agent to read and edit Swift source files as part of remediation.

Mitigation: Inspect proposed file changes as normal code review output and approve only changes that preserve intended behavior.

## Reference(s):

- [Swift 6.2 Concurrency Reference](references/swift-6-2-concurrency.md)
- [SwiftUI Concurrency Tour](references/swiftui-concurrency-tour-wwdc.md)
- [ClawHub Skill Page](https://clawhub.ai/steipete/skills/swift-concurrency-expert)
- [ClawHub Publisher Profile](https://clawhub.ai/user/steipete)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with Swift code examples and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose edits to Swift source files when asked to remediate concurrency issues.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
