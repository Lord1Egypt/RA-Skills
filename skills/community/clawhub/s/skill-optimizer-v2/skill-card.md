## Description:

Skill Optimizer evaluates agent skill files against SKILL-STANDARD-v3.md, scores metadata and structure, checks referenced template files, and returns improvement suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lj22503](https://clawhub.ai/user/lj22503)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to audit new or changed agent skills, batch-check skill quality, validate referenced template and script files, and produce concrete optimization suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests write and command-execution permissions beyond its stated read-only auditing behavior.

Mitigation: Run it with the narrowest permissions available and grant write access only for explicit, user-directed edits.

Risk: Broad activation triggers may cause the skill to run during unrelated skill discussions.

Mitigation: Confirm the target skill and intended audit action before executing scripts or applying recommendations.

Risk: Template-file validation and quality scoring can be mistaken for a complete safety review.

Mitigation: Treat reports as advisory and perform separate human review and security scanning before release.

## Reference(s):

- [Skill page](https://clawhub.ai/lj22503/skills/skill-optimizer-v2)
- [Publisher profile](https://clawhub.ai/user/lj22503)
- [Evaluation checklist](references/checklist.md)
- [Template validation script](scripts/check-templates.py)
- [Skill optimization script](scripts/optimize-skill.py)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style quality reports with command examples and structured recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include metadata checks, structure checks, quality scores, ratings, and prioritized suggestions.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
