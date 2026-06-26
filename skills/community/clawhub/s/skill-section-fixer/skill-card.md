## Description: <br>
Skill Section Fixer repairs skill documentation by adding missing required SKILL.md sections and frontmatter fields, with single-skill, batch, dry-run, and skip modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xukaitai321300-ctrl](https://clawhub.ai/user/xukaitai321300-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to repair WorkBuddy or ClawHub skill packages so their SKILL.md files include required sections and metadata. It is intended for single-skill cleanup, batch repair of a skills directory, and dry-run previews before rewriting files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch mode can rewrite many installed skills without built-in confirmation or rollback. <br>
Mitigation: Run dry-run first, inspect the planned file count and changes, and use it only on a backed-up, intended skills directory. <br>
Risk: Generated repairs can add generic or inaccurate sections and metadata to skill documentation. <br>
Mitigation: Review the edited SKILL.md files before deploying or publishing the repaired skills. <br>


## Reference(s): <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/xukaitai321300-ctrl/skill-section-fixer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with bash command examples; script execution produces terminal summaries and rewritten SKILL.md files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run mode previews planned changes; batch mode can rewrite many SKILL.md files.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
