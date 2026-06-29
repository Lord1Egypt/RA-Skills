## Description: <br>
A behavior-shaping agent skill that activates under repeated failure, low-quality completion, or explicit pressure prompts to push agents toward evidence-backed delivery using Journey to the West role personas, pressure escalation, and verification routines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ebandao777-oss](https://clawhub.ai/user/ebandao777-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to make coding agents more persistent, evidence-driven, and explicit about verification when they are stuck, passive, or claiming completion without proof. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is strongly opinionated and can persistently steer an agent's tone, workflow, and task-management behavior. <br>
Mitigation: Install it only when that behavior is desired, review data/config.json, and disable always_on or use /pua:off when the behavior should not persist. <br>
Risk: Harness verification can involve shell-based commands from task contracts. <br>
Mitigation: Do not run harness verification on untrusted contracts; inspect commands before execution and restrict use to trusted workspaces. <br>
Risk: The data/ files may retain behavioral or project memory across sessions. <br>
Mitigation: Review retained data files before sharing the workspace and delete or sanitize them when persistence is not needed. <br>
Risk: The release is tagged as requiring OAuth tokens or sensitive credentials. <br>
Mitigation: Use only in trusted environments and avoid exposing credentials to skill-managed logs, retained state, or generated reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ebandao777-oss/xuanzang-skill) <br>
- [README.md](README.md) <br>
- [QUICKSTART.md](QUICKSTART.md) <br>
- [REFERENCE.md](REFERENCE.md) <br>
- [Role router](references/role-router.md) <br>
- [Harness governance](references/harness-governance.md) <br>
- [Evolution protocol](references/evolution-protocol.md) <br>
- [Platform commands](references/platform-commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with command snippets and JSON-backed state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update data/ state files and propose harness verification commands when active.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact frontmatter reports 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
