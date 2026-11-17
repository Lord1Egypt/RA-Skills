## Description:

Helps create vvvv gamma editor extensions with .HDE.vl file naming, Command node registration, editor window setup, docking with WindowFactory, and VL.Lang Session API access for hovered or selected nodes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tebjan](https://clawhub.ai/user/tebjan)

### License/Terms of Use:

CC-BY-SA-4.0

## Use Case:

Developers and engineers use this skill when building vvvv gamma editor plugins, custom tooling windows, or editor workflow automation. It guides extension file naming, required NuGet references, command registration, window docking, and access to editor session data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated editor extensions can automate the vvvv editor and read or write pins in the active session.

Mitigation: Review generated .HDE.vl extension code and keyboard shortcuts before opening or running it in the editor.

Risk: A runtime error in one Command node can affect other commands in the same .HDE.vl document.

Mitigation: Review command grouping and test generated commands in the editor before relying on them in a workflow.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown with code-oriented guidance and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe .HDE.vl naming, VL.HDE and VL.Lang references, Command node settings, keyboard shortcuts, window types, and current editor-only limitations.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; skill frontmatter metadata version is 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
