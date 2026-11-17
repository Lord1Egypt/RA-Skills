## Description:

Compile and package Unreal Engine projects from the command line, including Windows, Android, and iOS packaging, cooking, solution builds, pak generation, editor commands, and build status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentwilliam](https://clawhub.ai/user/vincentwilliam)

### License/Terms of Use:


## Use Case:

Developers and build engineers use this skill to generate UnrealBuildTool, AutomationTool, PowerShell, and IDE-oriented guidance for building, packaging, and troubleshooting Unreal Engine projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hardcoded SilverPalace paths and target names may not match the user's Unreal Engine project.

Mitigation: Confirm project paths, target names, and platform settings before running generated build or packaging commands.

Risk: Troubleshooting guidance includes cache deletion and IDE automation actions that can affect local build state.

Mitigation: Treat cache deletion and IDE automation as manual troubleshooting steps and review them before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vincentwilliam/skills/ue-build-package)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with bash and PowerShell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project-specific paths and target names may need adjustment before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
