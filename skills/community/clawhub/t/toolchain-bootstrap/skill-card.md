## Description: <br>
Initializes a new OpenClaw container by downloading a prebuilt toolchain archive, extracting it to /workspace, configuring PATH and related environment variables, and verifying installed development tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[turinfohlen](https://clawhub.ai/user/turinfohlen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to bootstrap language runtimes and build tools in fresh OpenClaw development containers with a single setup command. It also supports verifying the installed toolchain and listing available tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow downloads and extracts a large external executable archive into /workspace. <br>
Mitigation: Use it mainly in fresh or disposable development containers, and only after trusting the TurinFohlen/openclaw-toolchain release identified in the evidence. <br>
Risk: The setup flow changes shell startup behavior by adding toolchain paths and environment variables to ~/.bashrc when writable. <br>
Mitigation: Review the generated /workspace/.toolchain_env and ~/.bashrc changes before relying on future shell sessions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/turinfohlen/toolchain-bootstrap) <br>
- [OpenClaw Toolchain Repository](https://github.com/TurinFohlen/openclaw-toolchain) <br>
- [Toolchain Archive Release](https://github.com/TurinFohlen/openclaw-toolchain/releases/download/v2.0/toolchain_v2.tar.gz) <br>
- [Environment Template Reference](references/env-template.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal status text with shell commands and environment variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes toolchain environment variables to /workspace/.toolchain_env and may append them to ~/.bashrc.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, skill.toml, and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
