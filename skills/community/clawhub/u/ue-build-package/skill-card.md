## Description: <br>
Helps agents compile and package Unreal Engine projects for Windows, Android, and iOS using UnrealBuildTool, AutomationTool, Rider, and related status checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentwilliam](https://clawhub.ai/user/vincentwilliam) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and build engineers use this skill to have an agent produce Unreal Engine build, packaging, and status-check commands for local projects. It is useful for command-line builds, platform packaging, Rider or Visual Studio workflows, and troubleshooting build output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hardcoded project paths, target names, platform choices, and cleanup steps may be incorrect for the user's local Unreal Engine project. <br>
Mitigation: Review every generated command, path, target, platform, Rider automation step, and cleanup action before allowing an agent to run it. <br>
Risk: Build and packaging commands can modify project outputs, logs, caches, staged builds, or local binaries. <br>
Mitigation: Run commands only in the intended project workspace and confirm the affected directories before executing build, package, or cache-cleaning operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vincentwilliam/ue-build-package) <br>
- [Publisher profile](https://clawhub.ai/user/vincentwilliam) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and PowerShell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are project-specific and may include hardcoded Unreal Engine paths, target names, platforms, and local cleanup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
