## Description: <br>
x-env helps agents install and manage x-cmd packages, language runtimes, command-line tools, software versions, upgrades, cleanup, paths, and dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lunrenyi](https://clawhub.ai/user/lunrenyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to have an agent propose and run x-cmd environment commands for installing, temporarily trying, upgrading, removing, and inspecting local runtimes and CLI tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package-management commands can install, update, remove, or clean up local software. <br>
Mitigation: Require explicit user approval before running installs, removals, cleanup, or upgrades. <br>
Risk: Remote installation methods can execute downloaded code, especially curl-to-shell workflows. <br>
Mitigation: Prefer Homebrew or a reviewed install script, and avoid curl-to-shell in sensitive environments. <br>
Risk: Persistent environment changes can affect later shell sessions and tool resolution. <br>
Mitigation: Use temporary try commands when testing and verify paths or dependencies before making changes persistent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lunrenyi/x-env) <br>
- [x-env repository](https://github.com/x-bash/env) <br>
- [Installation guide](data/install.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
