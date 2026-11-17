## Description:

Rhino3D plugin and script development with the RhinoCommon SDK: .rhp plugins and commands, Grasshopper .gha components, Eto panels, dialogs and options pages, user data and document persistence, display conduits, render engine integration, Python scripting, and yak packaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhauga](https://clawhub.ai/user/jhauga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, debug, package, and ship Rhino3D plugins, Grasshopper components, Rhino Python scripts, and related UI or persistence features.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install and build examples may fetch NuGet or Python dependencies.

Mitigation: Pin dependency versions before running copied commands and review generated project files before building.

Risk: Yak login and push commands can publish packages or use cached credentials.

Mitigation: Run publishing commands only from a trusted environment after confirming the package source, name, and version.

Risk: Generated Rhino project settings can affect plugin loading, packaging, and user data behavior.

Mitigation: Inspect .csproj, manifest, GUID, and persistence changes before release and test them in the intended Rhino version.

## Reference(s):

- [Plugin Project Template](assets/plugin-project-template.md)
- [UI Patterns](assets/ui-patterns.md)
- [Persistence and User Data](scripts/persistence-and-userdata.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code blocks, project scaffolding, configuration snippets, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated code, commands, and project files should be reviewed, pinned where dependencies are involved, and verified in the target Rhino environment before publishing.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
