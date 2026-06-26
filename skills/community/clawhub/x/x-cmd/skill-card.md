## Description: <br>
x-cmd helps agents load the x-cmd shell environment, discover x-cmd skills, and install portable CLI tools through x env or pixi. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwinjhlee](https://clawhub.ai/user/edwinjhlee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent operators use this skill to prepare x-cmd in a shell session, browse x-cmd capabilities, and install portable development tools without system-wide package changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill loads x-cmd paths into the active shell, which can change which executables are resolved first. <br>
Mitigation: Load x-cmd only in sessions where the user approves the PATH change, and verify commands with shell path inspection when working in sensitive environments. <br>
Risk: Installer and package workflows download code from remote sources. <br>
Mitigation: Prefer Homebrew or a reviewed installer, avoid curl-to-shell in sensitive environments, and approve package installs deliberately. <br>


## Reference(s): <br>
- [ClawHub x-cmd listing](https://clawhub.ai/edwinjhlee/x-cmd) <br>
- [x-cmd repository](https://github.com/x-cmd-skill/x-cmd) <br>
- [x-cmd website](https://www.x-cmd.com) <br>
- [x-cmd LLM reference](https://www.x-cmd.com/llms.txt) <br>
- [Installation guide](data/install.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and installation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend local PATH loading and user-local package installation steps.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
