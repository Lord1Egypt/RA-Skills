## Description:

Refactors code within an approved file scope, captures a test baseline, and verifies changes with regression tests and scope checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengfr](https://clawhub.ai/user/zengfr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to refactor code within an approved file scope while preserving behavior. It guides baseline capture, staged refactoring, regression testing, and scope and static checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment marks the skill suspicious because repeated unversioned `npx tsx` commands may download and run an unpinned package when it is not installed locally; the scan was partial and some referenced paths were missing.

Mitigation: Consider the install risk before proceeding. Use a pinned, locally installed `tsx` dependency to reduce the package-resolution risk identified by the scanner.

## Reference(s):

- [Server-resolved source repository](https://github.com/zengfr/AutoCoding/tree/main/docs/generated-skills/ultravibe-refactor)
- [Ultravibe Refactor on ClawHub](https://clawhub.ai/zengfr/skills/ultravibe-refactor)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code changes, JSON reports]

**Output Format:** [Markdown workflow instructions; code changes and JSON reports during execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Refactoring is scoped to an approved file whitelist and checked through staged test and guard gates.]

## Skill Version(s):

0.1.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
