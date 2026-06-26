## Description: <br>
Efficiently manage and interact with Umbrel proxy services for Docker containers by discovering running services, mapping internal Docker IPs to accessible host ports, and updating OpenClaw config. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gmoranxyz](https://clawhub.ai/user/gmoranxyz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and administrators managing Umbrel/OpenClaw hosts use this skill to discover Umbrel app proxy services, map accessible local ports, test connectivity, and update OpenClaw plugin configuration after restarts or setup changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sync commands can rewrite local OpenClaw plugin service URLs based on discovered or bundled mappings. <br>
Mitigation: Run the skill only on an Umbrel/OpenClaw host you control, back up OpenClaw configuration first, and review proposed mappings before applying changes. <br>
Risk: Broad Docker service discovery can expose local service topology and lead to incorrect mappings if the environment is unexpected. <br>
Mitigation: Prefer discovery-only or connectivity-test commands first, and do not use mappings from untrusted sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gmoranxyz/umbrel-proxy) <br>
- [Publisher profile](https://clawhub.ai/user/gmoranxyz) <br>
- [README.md](README.md) <br>
- [CHANGELOG.md](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and references to bundled scripts and configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may discover local Umbrel services and update OpenClaw configuration when executed by the operator.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence, package.json, CHANGELOG, target metadata; SKILL.md frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
