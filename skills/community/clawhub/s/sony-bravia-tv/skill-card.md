## Description: <br>
Control a Sony Bravia TV on the local network for power, volume, app launching, playback, status checks, and remote navigation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssupppp](https://clawhub.ai/user/ssupppp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and smart-home developers use this skill to let an agent control a configured Sony Bravia TV through local-network commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can issue disruptive TV actions such as power off, app switching, or long remote-button sequences. <br>
Mitigation: Require user confirmation for disruptive actions before running the command. <br>
Risk: The Sony TV pre-shared key and generated .env file can allow control of the configured TV. <br>
Mitigation: Keep SONY_TV_PSK private and avoid committing or sharing the generated .env file. <br>
Risk: Commands control a TV on the local network and may fail or target the wrong device if network settings are stale. <br>
Mitigation: Use the skill only on a trusted local network and verify SONY_TV_IP and SONY_TV_MAC during setup. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ssupppp/sony-bravia-tv) <br>
- [README](artifact/README.md) <br>
- [Sony Bravia Known App URIs](artifact/references/app-uris.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports command results and connection errors from the local TV control script.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
