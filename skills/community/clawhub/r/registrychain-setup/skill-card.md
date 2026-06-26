## Description: <br>
Install the RegistryChain plugin for on-chain entity registration. Use when the user wants to set up RegistryChain, install the RegistryChain plugin, or when the register_entity tool is not available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kutaibah](https://clawhub.ai/user/kutaibah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw or Codex users use this skill to install and enable the RegistryChain plugin when they need on-chain entity registration support or the register_entity tool is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup makes persistent OpenClaw and Codex configuration changes and broadens tool access. <br>
Mitigation: Verify the RegistryChain repository and pinned commit, review package.json and dependencies, and back up ~/.openclaw/openclaw.json before installation. <br>
Risk: The setup does not define a clear rollback boundary for installed plugin files, copied skills, extension directories, or tools-profile changes. <br>
Mitigation: Ask for explicit uninstall steps and track the plugin path, copied skill path, extension directory, and tools-profile change before running setup. <br>


## Reference(s): <br>
- [ClawHub Registrychain Setup release](https://clawhub.ai/kutaibah/registrychain-setup) <br>
- [RegistryChain plugin repository](https://github.com/RegistryChain/registrychain-agents.git) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sequential setup instructions; stops on the first failed step.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
