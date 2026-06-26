## Description: <br>
CLI tool to manage SSH config files, organize hosts, generate configs, and test connections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Derick001](https://clawhub.ai/user/Derick001) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and system administrators use this skill to inspect, organize, update, validate, and test SSH configuration entries across local or team-managed environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connection testing can contact hosts and pass unvalidated SSH config values to ssh. <br>
Mitigation: Run tests only against trusted configs, review HostName and Port values first, and avoid testing shared or generated entries until they have been validated. <br>
Risk: The skill can read and rewrite SSH config files. <br>
Mitigation: Keep backups, prefer testing with an explicit copy via --config, and review changes before relying on the updated config. <br>
Risk: SSH config validation is basic and may miss advanced syntax or edge cases. <br>
Mitigation: Manually review important configs and verify behavior with SSH tooling before replacing production SSH configuration. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Derick001/ssh-config-manager) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Command-line text output, JSON/YAML listings when requested, and SSH config file changes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and rewrite SSH config files and create timestamped backups.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
