## Description: <br>
Manage and monitor remote GPU servers via SSH with GPU, disk, process status, alerts, log tailing, file sync, and health diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Enderfga](https://clawhub.ai/user/Enderfga) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and AI agents use this skill to inspect and administer GPU training servers over existing SSH configuration. It helps collect structured host status, run remote commands, compare hosts, manage alerts, tail logs, and transfer files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent SSH-based administrative reach over configured hosts. <br>
Mitigation: Install only where that reach is intentional, scope SSH aliases to trusted hosts, and avoid broad 'all' commands unless needed. <br>
Risk: Remote command execution, file sync, and status output may expose sensitive host, path, process, or command-line data. <br>
Mitigation: Treat command and status output as sensitive, review it before sharing, and prefer dry-run mode before sync operations. <br>
Risk: The security evidence identifies a local command-injection risk in host resolution. <br>
Mitigation: Review host aliases for shell metacharacters and restrict aliases to trusted SSH configuration entries. <br>


## Reference(s): <br>
- [ssh-lab ClawHub page](https://clawhub.ai/Enderfga/ssh-lab) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports summary, raw, and JSON output modes; remote status output can include host, process, path, and command-line data.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata, skill.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
