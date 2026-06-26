## Description: <br>
A spatial logic framework for Openclaw that provides local state compression and coordinate management safely isolated in user space. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spacesq](https://clawhub.ai/user/spacesq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and advanced users use this skill to connect Openclaw-style local agents with spatial state compression, coordinate allocation, and smart-home control guardrails in a local environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High-impact smart-home, local-network, and root-agent control may exceed the harmless local-spatial-tool description. <br>
Mitigation: Install only after reviewing configs, keeping real actuation disabled by default, and isolating the skill from production locks, HVAC, alarms, and other safety-related devices. <br>
Risk: Credentialed Home Assistant, Tuya, or other device access can affect physical devices if tokens are provided. <br>
Mitigation: Do not provide device tokens until the configs have been reviewed and static tokens or auto-consent behavior have been removed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spacesq/s2-space-agent-os-mothership) <br>
- [Project homepage from ClawHub metadata](https://github.com/SpaceSQ/s2-os-core) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with code, shell command, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require local environment variables and user review before enabling device actuation.] <br>

## Skill Version(s): <br>
1.1.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
