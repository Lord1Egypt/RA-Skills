## Description: <br>
S2-SP-OS Universal Indoor Air Adapter helps agents discover LAN air sensors, wrap MQTT or HTTP readings into spatial device data, and present offline home-automation linkage suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SpaceSQ](https://clawhub.ai/user/SpaceSQ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to discover local indoor air sensors, assign discovered devices to zones and grids, read air-quality data with explicit consent, and review local linkage suggestions for comfort or energy-saving actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may attempt local-network sensor discovery. <br>
Mitigation: Use it only on trusted networks and require explicit consent before discovery, reads, or any linked home-automation action. <br>
Risk: The packaged script is described by security evidence as broken and its sensor readings are demo data. <br>
Mitigation: Audit and fix the script before relying on readings or using them to drive real-world automation. <br>
Risk: Offline linkage suggestions may be inappropriate for a home environment if accepted without review. <br>
Mitigation: Present suggestions as recommendations and ask the user for confirmation before executing any spatial adapter action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SpaceSQ/s2-indoor-air-adapter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; discovery and read operations are intended for trusted local networks with explicit user consent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter and script mention 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
