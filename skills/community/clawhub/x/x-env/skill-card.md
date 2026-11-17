## Description:

x-env helps agents install and manage x-cmd software packages, programming language runtimes, command-line tools, versions, paths, dependencies, cleanup, and upgrades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lunrenyi](https://clawhub.ai/user/lunrenyi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide x-cmd environment and package management tasks, including installing runtimes and CLI tools, switching versions, inspecting installed paths and dependencies, cleaning unused packages, and upgrading software.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes an auto-install path that executes a remote shell script.

Mitigation: Prefer Homebrew or a downloaded-and-reviewed installer; only run the direct remote script in disposable environments with no secrets and explicit user consent.

Risk: Cleanup, removal, and upgrade-all commands can change the user's installed tools.

Mitigation: Confirm the target packages and installation scope before running cleanup, removal, or broad upgrade commands.

## Reference(s):

- [x-env repository](https://github.com/x-bash/env)
- [x-cmd installation guide](data/install.md)
- [x-cmd installer](https://get.x-cmd.com)
- [x-cmd release artifacts](https://github.com/x-cmd/release)
- [Conda package source](https://conda.prefix.dev)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include package names, version specifiers, installation method choices, cleanup commands, and verification steps.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
