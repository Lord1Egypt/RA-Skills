## Description: <br>
This skill helps agents analyze, repair, validate, and record improvements to existing skill files when defects, missing workflow steps, logic errors, or lessons learned are identified. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and skill maintainers use this skill to diagnose problems in existing skills, make scoped edits, run regression checks, and record the impact of changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent edits to skill files and memory notes when broad trigger phrases match. <br>
Mitigation: Use it only where skill-maintenance edits are intended, narrow the trigger conditions, and require a dry-run diff or explicit confirmation before applying changes. <br>
Risk: Incorrect repairs could introduce misleading rules or regressions into skills. <br>
Mitigation: Review diffs, run regression checks, and scan updated skills before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/skill-dev) <br>
- [Project homepage](https://github.com/bettermen/skill-dev-scene) <br>
- [README.md](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with proposed or applied file edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update SKILL.md, scripts, references, changelog, or MEMORY.md when the host agent permits edits.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
