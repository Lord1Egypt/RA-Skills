## Description: <br>
Initialize a minimal SwiftUI iOS app in the current directory by generating a single `.xcodeproj` with XcodeGen (no workspaces, packages, or tests unless explicitly requested). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ignaciocervino](https://clawhub.ai/user/ignaciocervino) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to initialize a clean, single-target SwiftUI iOS project in an intended working directory. It gathers the project name, deployment target, and optional bundle identifier, then creates minimal XcodeGen configuration and SwiftUI app files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes a new SwiftUI project into the current directory and runs the local XcodeGen binary. <br>
Mitigation: Use it only in an empty or intended project folder, and verify that XcodeGen is installed from a trusted source before execution. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated local project files and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a minimal project.yml, SwiftUI source files, Info.plist, and a single Xcode project in the current directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
