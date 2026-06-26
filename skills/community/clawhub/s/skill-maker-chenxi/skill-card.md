## Description: <br>
Creates and upgrades reusable agent skills, including new SKILL.md files and refinements to existing skill structure, triggers, and supporting resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChenXi-hub](https://clawhub.ai/user/ChenXi-hub) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to turn recurring conversations or workflows into reusable SKILL.md assets and to update existing skills with clearer structure, triggers, checks, and references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to read broad private context while extracting reusable workflows. <br>
Mitigation: Provide exact source ranges and exclude secrets or unrelated private material before using the skill. <br>
Risk: The skill can guide an agent to persistently create or update active skills under ~/.openclaw/skills. <br>
Mitigation: Require a preview before writes, review the generated SKILL.md, and back up existing skills before replacement. <br>


## Reference(s): <br>
- [Skill Maker Reference](reference/reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ChenXi-hub/skill-maker-chenxi) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance and SKILL.md draft content, sometimes with file paths or shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update persistent skill files under ~/.openclaw/skills when the user approves the proposed content.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
