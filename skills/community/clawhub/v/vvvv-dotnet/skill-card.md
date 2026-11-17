## Description:

Helps with .NET integration in vvvv gamma, including NuGet packages, library references, .csproj project configuration, the [assembly: ImportAsIs] attribute, vector type interop, and async patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tebjan](https://clawhub.ai/user/tebjan)

### License/Terms of Use:

CC-BY-SA-4.0

## Use Case:

Developers and engineers use this skill when building or maintaining vvvv gamma .NET integrations, especially for package setup, project configuration, forwarded .NET libraries, vector interop, resource disposal, and async node patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to suggest external NuGet package sources or user-provided URLs.

Mitigation: Review feed URLs and any user-provided URLs before running commands that download packages or load remote content.

Risk: The skill can lead an agent to propose project-file edits and build commands.

Mitigation: Review generated .csproj, NuGet.config, and source changes before applying them, and run build commands in the intended project environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tebjan/skills/vvvv-dotnet)
- [vvvv package catalog](https://vvvv.org/packs)
- [NuGet package source](https://api.nuget.org/v3/index.json)
- [vvvv NuGet package source](https://teamcity.vvvv.org/guestAuth/app/nuget/v1/FeedService.svc/)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose .NET project edits, NuGet configuration, build commands, and vvvv gamma integration patterns.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter metadata.version reports 1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
