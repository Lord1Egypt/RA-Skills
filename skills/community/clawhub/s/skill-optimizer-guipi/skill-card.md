## Description: <br>
A WorkBuddy agent skill that helps users update and improve existing skills by diagnosing gaps, applying minimal edits, updating version records, and preserving lessons learned. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guipi888](https://clawhub.ai/user/guipi888) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and skill maintainers use this skill to repair workflow gaps, add or revise rules, and capture operational lessons in existing WorkBuddy skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is intended to modify existing installed skills, so incorrect edits could damage behavior or overwrite useful rules. <br>
Mitigation: Require an explicit target skill, read the current SKILL.md before editing, review a proposed diff before any write, and keep backups or version control. <br>
Risk: Broad trigger phrases can cause the skill to activate when no skill edit was intended. <br>
Mitigation: Confirm the user's intent and target skill before making changes, especially for short requests about skill problems or lessons learned. <br>
Risk: Captured lessons may be context-specific or misleading if written into reusable skill logic without review. <br>
Mitigation: Keep changes minimal, verify rendered Markdown and version records after editing, and store incident context in pitfalls/reference files. <br>


## Reference(s): <br>
- [修改规范](references/修改规范.md) <br>
- [踩坑总库](references/踩坑总库.md) <br>
- [优化经验](references/优化经验.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline commands and proposed file edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose updates to SKILL.md, version records, and pitfalls/reference files.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
