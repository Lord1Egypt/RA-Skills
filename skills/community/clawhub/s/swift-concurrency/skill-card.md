## Description:

Provides expert guidance on Swift Concurrency, including async/await, actors, tasks, Sendable, data-race safety, migration, and concurrency-related diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soponcd](https://clawhub.ai/user/soponcd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose Swift Concurrency issues, choose safe async/await and actor patterns, and plan Swift 6 migration work with appropriate project-setting checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advice may depend on Swift language mode, strict concurrency checking, upcoming features, or default actor isolation settings.

Mitigation: Inspect Package.swift or Xcode project settings and confirm unknown build settings before applying migration-sensitive fixes.

Risk: The artifact refers to helper reference files that are not included, which can limit topic-specific depth.

Mitigation: Use the main skill guidance as the authoritative available source and fall back to developer confirmation or external documentation when a referenced helper file is unavailable.

Risk: The skill may read or search Swift project files to tailor concurrency advice.

Mitigation: Review proposed file reads and searches in sensitive repositories and avoid exposing unrelated proprietary code when only configuration details are needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/soponcd/skills/swift-concurrency)
- [Swift Concurrency Course](https://www.swiftconcurrencycourse.com?utm_source=github&utm_medium=agent-skill&utm_campaign=skill-footer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Swift code snippets and project inspection commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask for Swift language mode, strict concurrency settings, default actor isolation, and related project configuration before giving migration-sensitive advice.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
