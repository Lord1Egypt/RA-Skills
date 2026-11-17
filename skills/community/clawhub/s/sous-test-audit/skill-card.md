## Description:

Decide whether a test earns its place. Use before writing a new test, when reviewing a diff that adds or deletes tests, when a suite is slow or flaky, or when asked to "clean up tests". Gates new tests on the behavior they prove, flags junk patterns, and requires evidence before any test is deleted.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orensegal](https://clawhub.ai/user/orensegal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to decide whether tests prove observable behavior, identify weak or redundant tests, and document evidence before deleting tests. It also helps verify that test runs executed the expected number of tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inspection was partial, and one referenced path was missing from the package, so the clean verdict does not confirm that all behavior was reviewed.

Mitigation: Review the complete skill and confirm the missing path is intentional before installing or executing it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/orensegal/skills/sous-test-audit)
- [Project homepage](https://github.com/OrenSegal/sous)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown audit summary with test identifiers, file and line references, and concise findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings depend on the tests and project diff being reviewed.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
