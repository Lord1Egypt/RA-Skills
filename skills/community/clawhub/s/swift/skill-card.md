## Description:

Writes, debugs, and optimizes Swift code across concurrency, ARC, optionals, generics, SwiftUI state, packages, testing, performance, and cross-platform interop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to write, review, refactor, debug, test, and optimize Swift code. It is especially useful for Swift concurrency diagnostics, ARC and memory issues, Codable failures, SwiftUI state problems, SwiftPM package issues, performance work, and macOS/Linux interop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use cross-session Swift preference and memory files under ~/Clawic/data/swift/.

Mitigation: Review or remove ~/Clawic/data/swift/config.yaml and ~/Clawic/data/swift/memory.md if cross-session personalization is not desired.

Risk: Swift code, shell commands, or configuration advice may be incorrect for a user's project, toolchain, or deployment target.

Mitigation: Review generated changes before applying them and validate with the relevant Swift build and test commands.

## Reference(s):

- [ClawHub Swift skill page](https://clawhub.ai/ivangdavila/skills/swift)
- [Clawic Swift skill page](https://clawic.com/skills/swift)
- [Swift skill definition](artifact/SKILL.md)
- [Swift setup and memory behavior](artifact/setup.md)
- [Swift memory template](artifact/memory-template.md)
- [Swift concurrency guidance](artifact/concurrency.md)
- [Swift debugging guidance](artifact/debugging.md)
- [Swift packages guidance](artifact/packages.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Swift code snippets, shell commands, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local Swift preferences and memory from ~/Clawic/data/swift/ when present.]

## Skill Version(s):

1.0.3 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
