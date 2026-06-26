## Description: <br>
Analyzes an existing Claude Code skill and designs an optimal rules/ file structure for lossless compression, conditional encapsulation, enrichment with templates or resources, and hardening of vague instructions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[VincentJiang06](https://clawhub.ai/user/VincentJiang06) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to plan and apply lossless restructuring of Claude Code skills, including moving content into rules modules, adding reusable resources, and clarifying ambiguous instructions. It can also run A/B comparisons to evaluate quality, token use, and timing between skill versions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose and apply file changes to another skill, which could introduce incorrect instructions if accepted without review. <br>
Mitigation: Use version control or backups, review the restructuring plan before approval, and scan the updated skill before deployment. <br>
Risk: The optional A/B comparison workflow can create benchmark files and spawn evaluation subagents for provided skill directories. <br>
Mitigation: Run comparison workflows only for directories you intend to evaluate and review generated benchmark, grading, and timing artifacts before relying on results. <br>


## Reference(s): <br>
- [Skill source on ClawHub](https://clawhub.ai/VincentJiang06/skill-rules-designer) <br>
- [JSON Schemas](references/schemas.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown plans and summaries with optional JSON benchmark files, rules files, templates, and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update skill files after user approval and may generate benchmark, timing, grading, comparison, or analysis JSON files during optional A/B evaluation.] <br>

## Skill Version(s): <br>
1.2.0 (source: ClawHub release evidence; SKILL.md frontmatter lists v1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
