## Description: <br>
Mirror Source Manager helps agents configure, switch, query, and restore package-manager download mirrors for npm, pip, Homebrew, apt, Go, Cargo, RubyGems, Docker, and related tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lunrenyi](https://clawhub.ai/user/lunrenyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when they need agent guidance or shell commands to inspect and change package-manager mirrors, especially to improve package download reliability or speed in regions where default registries are slow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Changing mirrors can persistently redirect future package downloads to a selected provider. <br>
Mitigation: Check the current mirror before changes, use trusted mirror providers, and require explicit confirmation before running set or unset commands. <br>
Risk: Installing x-cmd through curl-to-shell executes remote code before manual review. <br>
Mitigation: Prefer Homebrew or download and review the install script before execution, especially on sensitive machines. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lunrenyi/x-mirror) <br>
- [Skill Repository](https://github.com/x-cmd/x-mirror) <br>
- [Installation Guide](data/install.md) <br>
- [x-cmd Release Repository](https://github.com/x-cmd/release) <br>
- [x-cmd Install Endpoint](https://get.x-cmd.com) <br>
- [Conda Package Source](https://conda.prefix.dev) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that persistently modify package-manager mirror settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
