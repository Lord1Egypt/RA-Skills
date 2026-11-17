## Description:

Helps set up C# library projects that provide nodes to vvvv gamma, including project structure, assembly initialization, service registration, resource-provider factories, ImportAsIs configuration, project files, and dynamic node factories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tebjan](https://clawhub.ai/user/tebjan)

### License/Terms of Use:

CC-BY-SA-4.0

## Use Case:

Developers and engineers use this skill to create, organize, and publish vvvv gamma node libraries and VL packages with C# project scaffolding, node discovery conventions, service registration, help patches, and NuGet packaging guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The publishing workflow template uses mutable GitHub Actions references while handling a NuGet publishing key.

Mitigation: Pin GitHub Actions to reviewed commit SHAs, restrict workflow permissions, use a protected publishing environment, and scope or rotate the NuGet key.

Risk: Wildcard NuGet package versions can make generated library projects less reproducible and harder to review.

Mitigation: Prefer exact NuGet versions or lock files before using generated project configuration in a release workflow.

## Reference(s):

- [vvvv Node Factories documentation](https://thegraybook.vvvv.org/reference/extending/node-factories.html)
- [VL.IO.MQTT example library](https://github.com/vvvv/VL.IO.MQTT)
- [VL.Audio example library](https://github.com/vvvv/VL.Audio)
- [design-guidelines.md](artifact/design-guidelines.md)
- [publishing.md](artifact/publishing.md)
- [examples.md](artifact/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with C#, XML, YAML, and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include project structure examples, package metadata guidance, and publishing workflow templates]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
