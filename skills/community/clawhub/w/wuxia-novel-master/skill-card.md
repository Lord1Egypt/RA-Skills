## Description:

This skill coordinates an autonomous Chinese wuxia-novel creation workflow, from outline planning and volume drafting through review, revision, and final TXT formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kongzichixiangjiao](https://clawhub.ai/user/kongzichixiangjiao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creative-writing agents use this skill to generate or continue Chinese wuxia novels with autonomous outline creation, drafting, editorial review, revision, and final text formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect existing outline or manuscript files in the selected output directory.

Mitigation: Run it in a dedicated project directory containing only files intended for this writing workflow.

Risk: The workflow may create multiple generated text and Markdown files without asking for confirmation.

Mitigation: Choose an explicit output directory and review generated files before sharing or publishing them.

Risk: Generated fiction and editorial notes may contain continuity, style, or quality issues despite the built-in review workflow.

Mitigation: Review the final manuscript and intermediate review reports before treating the output as publication-ready.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kongzichixiangjiao/skills/wuxia-novel-master)
- [Skill README](artifact/README.md)
- [金庸 reference skill](artifact/references/01-金庸/SKILL.md)
- [古龙 reference skill](artifact/references/02-古龙/SKILL.md)
- [梁羽生 reference skill](artifact/references/03-梁羽生/SKILL.md)
- [温瑞安 reference skill](artifact/references/04-温瑞安/SKILL.md)
- [写手 reference skill](artifact/references/05-写手/SKILL.md)
- [检查 reference skill](artifact/references/06-检查/SKILL.md)
- [排版 reference skill](artifact/references/07-排版/SKILL.md)
- [Evaluation cases](artifact/evals/evals.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown drafts and review notes, plain-text manuscript files, and concise status messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create numbered intermediate manuscript files and a final TXT file in the selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
