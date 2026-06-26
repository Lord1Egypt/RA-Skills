## Description: <br>
VacuumControl teaches an OpenClaw agent how to install, authenticate, configure, and use roborock-cli to query and control Roborock vacuum cleaners. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jru001](https://clawhub.ai/user/jru001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide an agent through Roborock CLI setup, account authentication, device discovery, cleaning controls, diagnostics, and automation scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides use of an external CLI that authenticates to a Roborock account and stores account data in a local cache. <br>
Mitigation: Install and run the CLI only on a trusted machine, treat the authentication cache as sensitive, and remove the cache when access is no longer needed. <br>
Risk: Several commands physically control a vacuum cleaner, including starting cleaning, docking, dust collection, mop washing, volume, and do-not-disturb changes. <br>
Mitigation: Confirm the user's intent before control commands, check device status first, and avoid executing physical actions unless the requested action is clear. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jru001/roborock-2014) <br>
- [Roborock CLI command reference](references/commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes jq-oriented JSON parsing examples; authentication requires an interactive TTY.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence, released 2026-03-17) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
