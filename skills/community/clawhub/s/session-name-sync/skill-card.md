## Description: <br>
Bidirectionally syncs session names between Claude Code CLI/VSCode and cc-connect so both systems keep consistent names for the same sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangyanbo2007](https://clawhub.ai/user/zhangyanbo2007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Claude Code users who also use cc-connect/Feishu can use this skill to set, compare, bind, register, and synchronize session names across both storage systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and write local Claude Code session data and cc-connect session JSON. <br>
Mitigation: Install only if you trust the publisher, review the exact sessions to be changed, and back up ~/.cc-connect session JSON before sync or register operations. <br>
Risk: Register or sync workflows may perform bulk session changes and can require cc-connect daemon restarts. <br>
Mitigation: Require explicit user confirmation before bulk registration or daemon restarts, and avoid running it with unusual or untrusted cc-connect work_dir values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangyanbo2007/session-name-sync) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Release README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline Bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify local Claude Code JSONL files and cc-connect session JSON when the user confirms write actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
