## Description:

Native iOS and macOS apps in Swift 6 - SwiftUI, AppKit, SwiftData, concurrency, Swift Testing, XcodeGen, CallKit and audio, App Intents, devices, TestFlight, code signing, notarization. Use for any iPhone or Mac app, helper or CLI work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tenequm](https://clawhub.ai/user/tenequm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building iPhone, iPad, and Mac apps, helpers, or command-line tools can use this skill for practical Swift 6 guidance across app architecture, concurrency, persistence, testing, platform APIs, signing, and distribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Signing credentials or upload access could be exposed or used for an unintended app.

Mitigation: Keep signing keys outside repositories and authorize uploads only for the intended app.

Risk: Broad or permanent MCP permissions can grant more access than a project needs.

Mitigation: Prefer project-scoped, time-limited MCP permissions over permanent or all-agent grants.

Risk: Attribute-clearing commands or recording teardown can affect unintended files or leave capture running.

Mitigation: Apply attribute-clearing commands only to intended build bundles, and test recording shutdown before shipping.

## Reference(s):

- [Skill guide](SKILL.md)
- [Swift concurrency isolation](references/concurrency-isolation.md)
- [Swift concurrency tasks](references/concurrency-tasks.md)
- [SwiftData models and store](references/swiftdata-models.md)
- [iOS project setup](references/ios-project-setup.md)
- [iOS distribution](references/ios-distribution.md)
- [macOS distribution](references/macos-distribution.md)
- [Testing](references/testing.md)
- [Homepage (Clawdis metadata)](https://github.com/tenequm/skills/tree/main/skills/swift-dev)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Swift code, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task-focused guidance routed to the relevant iOS, macOS, or shared reference; examples may require adaptation to the target SDK and project.]

## Skill Version(s):

0.3.1 (source: frontmatter, CHANGELOG released 2026-11-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
