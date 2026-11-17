## Description:

Verification Gate guides agents through an eight-stage post-change verification checklist for build, type, lint, unit, end-to-end, real-runtime, security, and diff review gates before code is called ready.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cat-xierluo](https://clawhub.ai/user/cat-xierluo)

### License/Terms of Use:

MIT

## Use Case:

Developers and coding agents use this skill after feature work, major changes, refactors, bug fixes, or before PR creation to select and run verification checks for Tauri desktop, web, service, and skill projects. It emphasizes end-to-end functional checks and real-runtime validation before marking work ready.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some command examples use unpinned npx execution, which can download and run changing third-party packages during verification.

Mitigation: Replace unpinned npx commands with pinned, locked project dependencies before use.

Risk: Service verification may run tests against staging systems where credentials or data scope matter.

Mitigation: Use isolated staging data with scoped credentials and avoid production data when following the workflow.

Risk: The workflow includes diff and git-state review steps that can affect repository state if expanded into write operations.

Mitigation: Get explicit approval before changing git state and treat review commands as read-only unless a maintainer authorizes changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cat-xierluo/skills/verification-gate)
- [Publisher profile](https://clawhub.ai/user/cat-xierluo)
- [Project homepage](https://github.com/cat-xierluo/legal-skills)
- [Assertion Depth Guide](references/assertion-depth.md)
- [E2E Practice](references/e2e-practice.md)
- [Eight Phases Rationale](references/eight-phases-rationale.md)
- [Lessons from Practice](references/lessons-from-practice.md)
- [Test Pyramid](references/test-pyramid.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with command examples and verification report tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language workflow guidance for code verification gates across Tauri desktop, web, service, and skill projects.]

## Skill Version(s):

1.0.2 (source: frontmatter and changelog, released 2026-08-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
