## Description: <br>
Workspace memory and persona management subroutine for maintaining session continuity across MEMORY.md, SOUL.md, and IDENTITY.md. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawnjlewis](https://clawhub.ai/user/shawnjlewis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage persistent workspace memory and persona files for an agent. It supports user-invoked memory consolidation, proposed SOUL and IDENTITY updates, configurable auto-triggers, and audit-log review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently change agent memory, personality, and identity files, and the security scan reports a Review verdict because safety rules conflict in important places. <br>
Mitigation: Review before installing, start with the strict profile, keep auto-triggers disabled, and require confirmation for SOUL.md and IDENTITY.md writes. <br>
Risk: Memory consolidation can update MEMORY.md or memory/*.md without a separate confirmation when the user invokes the consolidation command or enables compatible triggers. <br>
Mitigation: Back up MEMORY.md, SOUL.md, and IDENTITY.md before activation and inspect skill_audit.log for unexpected reads, writes, trigger runs, or rejected paths. <br>
Risk: File and network restrictions are partly instruction-designed and depend on the host sandbox for enforcement. <br>
Mitigation: Run the skill in a sandboxed workspace, verify path-validation behavior, and avoid enabling High Autonomy unless unconfirmed persistent persona or identity changes are intentionally accepted. <br>


## Reference(s): <br>
- [Westworld Reverie ClawHub release](https://clawhub.ai/shawnjlewis/westworld-reverie) <br>
- [Configuration Reference](references/config-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown/text responses, command guidance, and workspace Markdown file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write MEMORY.md, SOUL.md, IDENTITY.md, memory/*.md, and skill_audit.log according to the selected security profile.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
