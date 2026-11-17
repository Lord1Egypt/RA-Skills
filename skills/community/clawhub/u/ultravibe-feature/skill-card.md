## Description:

Guides feature development through specification freeze, test-driven implementation, reverse validation, semantic comparison, and global checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengfr](https://clawhub.ai/user/zengfr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to plan and implement repository feature requests with explicit scope, test, and validation gates. It guides work through specification and validation reports, then requires tests, scope checks, and static checks to pass before completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repeated npx tsx commands may download and run an unpinned package; the security scan was incomplete.

Mitigation: Before installation, confirm that tsx is pinned and installed from a lockfile so a missing tool cannot trigger an implicit download.

## Reference(s):

- [Server-resolved source repository](https://github.com/zengfr/AutoCoding/tree/main/docs/generated-skills/ultravibe-feature)
- [ClawHub skill page](https://clawhub.ai/zengfr/skills/ultravibe-feature)

## Skill Output:

**Output Type(s):** [Code, Files, Guidance]

**Output Format:** [Source code changes and JSON specification, validation, and checkpoint reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Progresses through gated phases; completion requires tests, scope checks, and static checks to pass.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
