## Description:

Set up and run automated tests for vvvv gamma packages and C# nodes using VL.TestFramework, NUnit, VL patch assertions, and CI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tebjan](https://clawhub.ai/user/tebjan)

### License/Terms of Use:

CC-BY-SA-4.0

## Use Case:

Developers and engineers use this skill to create, run, and integrate automated tests for vvvv gamma packages, C# nodes, and .vl patches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated test workflows can execute project code when run in CI or shared projects.

Mitigation: Run tests only against trusted vvvv packages and patches, and review generated test code before execution.

Risk: Wildcard NuGet dependency versions can change test behavior over time.

Mitigation: Pin exact NuGet package versions and consider committing a lock file before using the workflow in CI.

## Reference(s):

- [VL.TestFramework API Reference](test-framework-reference.md)
- [ClawHub skill release](https://clawhub.ai/tebjan/skills/vvvv-testing)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with C#, XML, YAML, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CI setup guidance, NUnit test project examples, vvvv launch commands, and VL.TestFramework API usage.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
