## Description:

Set up debugging for vvvv gamma C# node projects by helping generate VS Code launch and task configurations, attach to a running vvvv process, configure Visual Studio debug profiles, and apply debugging best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tebjan](https://clawhub.ai/user/tebjan)

### License/Terms of Use:

CC-BY-SA-4.0

## Use Case:

Developers and engineers use this skill to set up debugger launch, attach, and build configurations for vvvv gamma C# node projects. It is intended for workspace-aware debugging setup where the agent inspects project files, asks configuration questions, and proposes local editor configuration files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect workspace structure and propose creating or updating local VS Code or Visual Studio debugging files.

Mitigation: Review generated launch, task, and profile configuration before applying it, especially paths, build commands, and debugger attach settings.

Risk: Using --package-repositories on a broad workspace with library submodules can trigger slow recompilation.

Mitigation: Avoid broad package repository paths unless needed; when enabled, point the option at the narrow package folder that should be scanned.

## Reference(s):

- [Vvvv Debugging ClawHub release page](https://clawhub.ai/tebjan/skills/vvvv-debugging)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local VS Code launch.json and tasks.json updates, Visual Studio launch profile settings, and debugging workflow guidance after user confirmation.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter metadata.version is 1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
