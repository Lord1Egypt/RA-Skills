## Description:

Transforms project experience into industrial-strength resume bullets with architectural depth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwaguai](https://clawhub.ai/user/wwaguai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn a code repository or pasted project description into stronger resume material. It scans or audits project details, asks for missing architectural and quantitative context, and produces bilingual resume bullets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read project repositories and some Git metadata during repository-based analysis.

Mitigation: Run it only on repositories you are comfortable exposing to the agent, and review any generated resume content before sharing it.

Risk: The skill keeps a persistent resume library in the user's home directory.

Mitigation: Review ~/.claude/resume-library.md periodically and remove sensitive project, employer, or career details that should not persist.

Risk: The release artifact bundles many unrelated tools in addition to the resume skill.

Mitigation: Inspect the package before installation and prefer a package that contains only the intended resume-project skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwaguai/skills/resume-project)
- [Skill instructions](artifact/skills/skills/resume-project/SKILL.md)
- [Skill README](artifact/skills/skills/resume-project/README.md)
- [Evaluation cases](artifact/skills/skills/resume-project/evals/evals.json)

## Skill Output:

**Output Type(s):** [analysis, markdown, guidance]

**Output Format:** [Markdown with bilingual resume bullets, targeted follow-up questions, topic labels, and TBD placeholders for unconfirmed metrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append persistent project records to ~/.claude/resume-library.md.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
