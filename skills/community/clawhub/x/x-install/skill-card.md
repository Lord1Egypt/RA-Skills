## Description: <br>
Software Installation Assistant uses x-cmd's install module to look up supported software, return installation commands, and explain installation options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lunrenyi](https://clawhub.ai/user/lunrenyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and shell users use this skill to query x-cmd installation recipes, list supported software, and choose installation commands before installing packages. It is useful when an agent needs to propose or explain install commands with explicit user consent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation guidance may involve downloading and executing remote code, including an automatic curl-to-shell path. <br>
Mitigation: Prefer Homebrew or a download-review-execute workflow; avoid automatic curl-to-shell installation on sensitive machines unless the user explicitly accepts the supply-chain risk. <br>
Risk: x-cmd installation may leave user-local files or shell configuration changes after use. <br>
Mitigation: Use the documented user-local installation path and check shell configuration if x-cmd is later removed. <br>
Risk: An agent could propose software installation without adequate user intent. <br>
Mitigation: Require explicit user consent before installation and present the installation method so the user can choose or decline it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lunrenyi/x-install) <br>
- [x-cmd skill repository](https://github.com/x-cmd/skill) <br>
- [x-cmd Installation Guide](data/install.md) <br>
- [x-cmd release downloads](https://github.com/x-cmd/release) <br>
- [x-cmd installer endpoint](https://get.x-cmd.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that download or install software; installation method should be selected with user consent.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
