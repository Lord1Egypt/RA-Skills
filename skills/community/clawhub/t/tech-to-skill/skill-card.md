## Description:

Distills technical long-form content such as engineering notes, papers, and project docs into agent-callable skills with evidence indexing and temporal tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leogoat2004](https://clawhub.ai/user/leogoat2004)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert technical articles, papers, and project documentation into reusable agent skills with What, How, Why, evidence references, and timestamps. It is intended for source-faithful distillation workflows where users review candidate skills before files are generated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads user-selected files, repositories, or URLs and creates generated skill files, so unintended inputs or output locations could expose irrelevant content or overwrite nearby work.

Mitigation: Provide only the sources intended for inspection, choose a separate empty output directory, and review generated files before using or sharing them.

Risk: Generated skills may preserve source mistakes or omit context if candidates and evidence are not reviewed.

Mitigation: Review the candidate list, generated SKILL.md files, and evidence references before relying on the resulting skills.

Risk: The install command should be treated carefully like any third-party skill installation.

Mitigation: Prefer a pinned or verified release when available and inspect the skill contents before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leogoat2004/skills/tech-to-skill)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [longform-to-skill](artifact/sub-skills/longform-to-skill/SKILL.md)
- [paper-to-skill](artifact/sub-skills/paper-to-skill/SKILL.md)
- [project-docs-to-skill](artifact/sub-skills/project-docs-to-skill/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown skill files, evidence reference files, batch README content, and concise review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated skills to a user-specified output directory and requires user review of candidate skills and evidence files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
