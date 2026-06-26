## Description: <br>
Manage agent memory with Membase, a decentralized encrypted backup and restore system for agent memories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ibitnoah](https://clawhub.ai/user/ibitnoah) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw agents use this skill to back up, list, compare, restore, and inspect agent memory files through Membase-backed encrypted storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Secrets may be exposed through documented echo commands, visible password arguments, or unredacted status output. <br>
Mitigation: Avoid echoing secrets, avoid passing passwords directly in shell commands, and use JSON-disabled or redacted status output until secret handling is reviewed. <br>
Risk: Restore operations can write remote backup contents into local agent memory. <br>
Mitigation: Verify the backup ID and source, preserve the current workspace, and inspect backup differences before restoring. <br>
Risk: The provided artifact references a lib implementation that is not included in the package evidence. <br>
Mitigation: Request and review the complete package before trusting encryption, upload, download, and restore behavior. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ibitnoah/unibase-membase) <br>
- [Membase Documentation](https://github.com/unibaseio/membase) <br>
- [AgentSkills Specification](https://agentskills.io) <br>
- [OpenClaw Skills Guide](https://docs.openclaw.ai/tools/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text with optional JSON blocks and Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operations require Membase credentials and may require a backup password.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md metadata and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
