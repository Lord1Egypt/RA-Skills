## Description: <br>
Meta-skill for creating new agent skills — generates well-structured SKILL.md files with proper frontmatter, triggers, protocols, and rules. Use when building custom skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NakedoShadow](https://clawhub.ai/user/NakedoShadow) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to interview users about a repeatable workflow, generate a complete SKILL.md, and validate that the resulting skill has concrete triggers, prerequisites, security notes, rules, and output expectations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated skills can affect future agent behavior if their triggers are too broad, their instructions are ambiguous, or their requirements are not reviewed. <br>
Mitigation: Review every generated SKILL.md before enabling, testing, or publishing it, with attention to trigger scope, concrete instructions, prerequisites, and security considerations. <br>
Risk: Generated skills may include shell commands, network access, credential requirements, or high-impact actions in their instruction sections. <br>
Mitigation: Check generated commands, file and network access, credential handling, and approval requirements before installing or distributing the generated skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NakedoShadow/shadows-skill-factory) <br>
- [Publisher profile](https://clawhub.ai/user/NakedoShadow) <br>
- [OpenClaw homepage metadata](https://clawhub.ai/NakedoShadow) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown SKILL.md content with YAML frontmatter and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a complete skill instruction file for review before enabling, testing, or publishing.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata and SKILL.md body) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
