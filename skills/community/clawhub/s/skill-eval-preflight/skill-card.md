## Description:

Validate OpenClaw skills during authoring. Use when creating, revising, or preparing a skill for release and you need to scaffold `evals/` files, check readiness for a first eval pass, review whether the frontmatter description has clear trigger coverage, or generate static comparison artifacts before deeper runtime evaluation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stonechen1014](https://clawhub.ai/user/stonechen1014)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to prepare OpenClaw skills for release by scaffolding eval files, checking first-pass readiness, reviewing trigger coverage, and producing static comparison artifacts before deeper runtime evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled scripts can write comparison or run artifacts outside the intended skill folder if given a crafted run-group path.

Mitigation: Install only from a trusted author and use simple run-group names made from letters, digits, underscores, dots, or hyphens until output paths are constrained by the scripts.

## Reference(s):

- [Skill Eval File Formats](references/eval_format.md)
- [ClawHub Skill Release Page](https://clawhub.ai/stonechen1014/skills/skill-eval-preflight)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON files, Markdown]

**Output Format:** [Markdown guidance with shell commands plus JSON and Markdown eval artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create eval scaffolding, static run summaries, run metadata, and comparison artifacts under evals/.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
